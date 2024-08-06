import time
import requests
import random
import re
import pymysql
import pyperclip as pc

from hashlib import md5

mysql_connect = {
    "host": '192.168.100.212',
    "port": 3306,
    "user": 'root',
    "passwd": 'tiger_scm',
    "db": 'scm_global'
}

database_connect = pymysql.connect(
    host=mysql_connect["host"],
    user=mysql_connect["user"],
    passwd=mysql_connect["passwd"],
    port=mysql_connect["port"],
    db=mysql_connect['db'])

group_name = 'UserDefine_Common'
message = r'控件类型{valueArgs.ControlType}不支持'


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def translate_message(message):
    time.sleep(2)

    appid = '20230404001628097'
    appkey = 'LeUgrn2_LGjZ_UrHgG_d'
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


def insert_temp_message_resource(message, translate_message):
    search_sql = r"SELECT (CASE WHEN MAX(SEQUENCE_NUMBER) IS NULL THEN 0 ELSE MAX(SEQUENCE_NUMBER) END) AS SEQUENCE_NUMBER FROM vito_temp_sys_message_resource WHERE GROUP_NAME = '%s' ORDER BY SEQUENCE_NUMBER DESC" % group_name

    database_cursor = database_connect.cursor()
    database_cursor.execute(search_sql)
    database_result = database_cursor.fetchall()
    sequence_number = int(database_result[0][0]) + 1
    key = '%s_%s' % (group_name, str(int(sequence_number)).zfill(6))

    insert_sql = "INSERT vito_temp_sys_message_resource (GROUP_NAME, SEQUENCE_NUMBER, VIEW_TEXT_CH, VIEW_TEXT_EN, FILE_PATH, `KEY`) "
    insert_sql += "SELECT '%s', %s, '%s','%s','%s','%s' FROM DUAL " % (group_name, sequence_number, message, translate_message.replace("\'", "''"), '', key)
    insert_sql += "WHERE NOT EXISTS(SELECT 1 FROM vito_temp_sys_message_resource WHERE VIEW_TEXT_CH = '%s')" % message

    try:
        rowcount = database_cursor.execute(insert_sql)
        database_connect.commit()

        if rowcount > 0:
            return {
                "key": key,
                "text_cn": message,
                "text_en": translate_message
            }
    except Exception as error:
        database_connect.rollback()
    return None


def build_message_param(message_list):
    message_array = ["'%s'" % x for x in message_list]
    message_param = ','.join(message_array)
    return message_param


def get_database_message_key(sql):
    database_cursor = database_connect.cursor()
    database_cursor.execute(sql)
    database_result = database_cursor.fetchall()

    if len(database_result) <= 0:
        return {}

    result = {}
    for row in database_result:
        result[row[1]] = row[0]

    return result


def search_message_resource(message_list):
    result = {}

    sql_param = build_message_param(message_list)
    query_sys_message_resource_sql = 'SELECT RESOURCE_KEY, VIEW_TEXT FROM sys_message_resource WHERE VIEW_TEXT IN (%s)' % sql_param
    query_temp_sys_message_resource_sql = 'SELECT `Key`, VIEW_TEXT_CH FROM vito_temp_sys_message_resource WHERE VIEW_TEXT_CH IN (%s)' % sql_param

    resource_result = get_database_message_key(query_sys_message_resource_sql)
    temp_resource_result = get_database_message_key(query_temp_sys_message_resource_sql)

    for message_info in resource_result:
        result[message_info] = resource_result[message_info]

    for message_info in temp_resource_result:
        result[message_info] = temp_resource_result[message_info]

    result['货品'] = 'AppOrder_000365'

    return result


def build_message_sql(info):
    print("CALL T_MSG('%s','%s','%s');" % (info["key"], info["text_cn"], 'zh_cn'))
    print("CALL T_MSG('%s','%s','%s');" % (info["key"], info["text_en"], 'en_us'))


def split_replace():
    # regex_01_message_match = re.findall(r'({.*?})', message)
    regex_02_message_match = re.findall(r'([\u4e00-\u9fa5]+)', message)
    new_key_list = []
    temp_message = message
    message_key_list = search_message_resource(regex_02_message_match)
    for message_02 in regex_02_message_match:
        key = '' if message_02 not in message_key_list else message_key_list[message_02]
        if key is None or key == '':
            message_en = translate_message(message_02)
            message_key_info = insert_temp_message_resource(message_02, message_en)
            if message_key_info:
                key = message_key_info['key']
                new_key_list.append(message_key_info)

        temp_message = temp_message.replace(message_02, '{Context.B.R("%s", "%s")}' % (message_02, key))

    temp_message = '$"%s"' % temp_message
    pc.copy(temp_message)

    print("\n")
    print(temp_message)
    print("\n\n")
    for new_key in new_key_list:
        build_message_sql(new_key)


split_replace()
database_connect.close()

