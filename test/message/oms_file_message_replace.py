import re
import time
import requests
import random
import json
import pymysql

from hashlib import md5

group_name = 'Configuration_Common'
file_path = r'D:\quantum-scm\SCM\Service\SCM.OMS\SCM.OMS.Service\ReciptOrder\Import\ImportReceipt.cs'

mysql_connect = {
    "host": '192.168.100.212',
    "port": 3306,
    "user": 'root',
    "passwd": 'tiger_scm',
    "db": 'scm_global'
}

baidu_api_info = {
    'appid': '20230404001628097',
    'appkey': 'LeUgrn2_LGjZ_UrHgG_d'
}

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def translate_message(message, api_info):
    time.sleep(2)

    appid = api_info['appid']
    appkey = api_info['appkey']

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + message + str(salt) + appkey)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'appid': appid,
        'q': message,
        'from': 'zh',
        'to': 'en',
        'salt': salt,
        'sign': sign
    }

    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    response = requests.post(url, params=payload, headers=headers).json()

    if response and 'trans_result' in response and 'dst' in response['trans_result'][0]:
        return response['trans_result'][0]['dst']
    else:
        return None


def build_message_param(message_list):
    message_array = ["'%s'" % x for x in message_list]
    message_param = ','.join(message_array)
    return message_param


def search_message_resource(message_list, database_connect):
    result = {}
    sql_param = build_message_param(message_list)

    sql = 'SELECT RESOURCE_KEY, VIEW_TEXT FROM sys_message_resource WHERE VIEW_TEXT IN (%s)' % sql_param

    database_cursor = database_connect.cursor()
    database_cursor.execute(sql)
    database_result = database_cursor.fetchall()

    if len(database_result) <= 0:
        return result

    for row in database_result:
        result[row[1]] = row[0]

    return result


def search_temp_message_resource(message_list, database_connect):
    result = {}
    sql_param = build_message_param(message_list)

    sql = 'SELECT GROUP_NAME, SEQUENCE_NUMBER, `KEY`, VIEW_TEXT_CH, VIEW_TEXT_EN ' \
          'FROM vito_temp_sys_message_resource ' \
          'WHERE VIEW_TEXT_CH IN (%s)' % sql_param

    database_cursor = database_connect.cursor()
    database_cursor.execute(sql)
    database_result = database_cursor.fetchall()

    if len(database_result) <= 0:
        return result

    for row in database_result:
        result[row[3]] = row[2]

    return result


def get_message_list_by_file():
    result = []
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()

            if not line:
                break

            match_list = re.compile(r'"(.*)"').findall(line)
            if not match_list or len(match_list) <= 0:
                continue

            if '("' in match_list[0]:
                match_match_list = re.compile(r'("[\u4e00-\u9fa5a-zA-Z0-9,.:]+")').findall(match_list[0])
            else:
                match_match_list = match_list

            for match in match_match_list:
                search_list = re.compile(r'[\u4e00-\u9fa5]+').search(match)

                if not search_list or len(search_list.groups()) < 0:
                    continue

                result.append(match.replace('"', ''))

    return result


def build_message_sql(key, message, message_en):
    result = []
    result.append("CALL T_MSG('%s','%s','%s');" % (key, message, 'zh_cn'))
    result.append("CALL T_MSG('%s','%s','%s');" % (key, message_en, 'en_us'))

    return result


def insert_temp_message_resource(message, message_en, database_connect):
    search_sql = """SELECT (CASE WHEN MAX(SEQUENCE_NUMBER) IS NULL THEN 0 ELSE MAX(SEQUENCE_NUMBER) END) AS SEQUENCE_NUMBER 
                   FROM vito_temp_sys_message_resource 
                   WHERE GROUP_NAME = '%s' ORDER BY SEQUENCE_NUMBER DESC""" % group_name
    
    database_cursor = database_connect.cursor()
    database_cursor.execute(search_sql)
    database_result = database_cursor.fetchall()
    sequence_number = int(database_result[0][0]) + 1
    key = '%s_%s' % (group_name, str(int(sequence_number)).zfill(6))

    insert_sql = """INSERT vito_temp_sys_message_resource (GROUP_NAME, SEQUENCE_NUMBER, VIEW_TEXT_CH, VIEW_TEXT_EN, FILE_PATH, `KEY`)
                    SELECT '%s', %s, '%s','%s','%s','%s' FROM DUAL " % (group_name, sequence_number, message, message_en.replace("\'", "''"), '', key)
                    WHERE NOT EXISTS(SELECT 1 FROM vito_temp_sys_message_resource WHERE VIEW_TEXT_CH = '%s')""" % message

    try:
        rowcount = database_cursor.execute(insert_sql)
        database_connect.commit()

        if rowcount > 0:
            return {
                "key": key,
                "text_ch": message,
                "text_en": message_en
            }
    except Exception as error:
        database_connect.rollback()


database_connect = pymysql.connect(host=mysql_connect["host"],
                                   user=mysql_connect["user"],
                                   passwd=mysql_connect["passwd"],
                                   port=mysql_connect["port"],
                                   db=mysql_connect['db'])

file_message_list = get_message_list_by_file()
sys_message_info_list = search_message_resource(file_message_list, database_connect)
temp_message_info_list = search_temp_message_resource(file_message_list, database_connect)

for message_key in temp_message_info_list:
    if message_key not in sys_message_info_list:
        sys_message_info_list[message_key] = temp_message_info_list[message_key]

replace_message_list = []
for message in file_message_list:
    exists_message_list = list(filter(lambda x: x['message'] == message, replace_message_list))
    
    if len(exists_message_list > 0):
        continue
    
    if message in sys_message_info_list:
        replace_message_list.append({
            'message': message,
            'key': sys_message_info_list[message]
        })
    else:
        message_en = translate_message(message, baidu_api_info)
        message_info = insert_temp_message_resource(message, message_en, database_connect)

        replace_message_list.append({
            'message': message,
            'key': message_info['key'],
            'sql': build_message_sql(message_info['key'], message, message_en)
        })

file_content = ''
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

for message_info in replace_message_list:
    old_message = '"%s"' % message_info['message']
    new_message = '%s, "%s"' % (old_message, message_info['key'])
    file_content = file_content.replace(old_message, new_message)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_content)

    if 'sql' in message_info:
        for sql in message_info['sql']:
            print(sql)
    print('\n')

database_connect.close()

print(file_path)