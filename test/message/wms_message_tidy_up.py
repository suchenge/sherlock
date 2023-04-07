import re
import os
import time
import random
import requests
import json
import math
import threading

from datetime import datetime
from hashlib import md5

baidu_api_info_su = {
    'appid': '20230329001619824',
    'appkey': 'DrUuH1mrCrXcpXrLkG4H'
}

baidu_api_info_chong = {
    'appid': '20230404001627962',
    'appkey': 'cbCP6d0nL7QEnxw1z_q9'
}

baidu_api_info_jiang = {
    'appid': '20230404001627965',
    'appkey': 'qrnjlaJiI4Mxp42LNjwB'
}

baidu_api_info_li = {
    'appid': '20230404001627983',
    'appkey': '39y0siVZ9Q2TiJRTlBVa'
}

baidu_api_info_fu = {
    'appid': '20230404001628083',
    'appkey': 'DmxUIqZMqNOzE1GAEnwO'
}

baidu_api_info_zhang = {
    'appid': '20230404001628088',
    'appkey': 'MBzHwumBfGBvlZgskVbU'
}

baidu_api_info_zuo = {
    'appid': '20230404001628097',
    'appkey': 'LeUgrn2_LGjZ_UrHgG_d'
}

baidu_api_info_current = baidu_api_info_chong
baidu_api_info_list = [baidu_api_info_chong, baidu_api_info_jiang, baidu_api_info_li, baidu_api_info_fu, baidu_api_info_zhang, baidu_api_info_zuo]


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def translate_message(message, baidu_api_info):
    time.sleep(2)

    appid = baidu_api_info['appid']
    appkey = baidu_api_info['appkey']

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


file_path = 'E:\\Download\\total.txt'
new_file_path = file_path.replace('.txt', '_new.txt')
message_file_path = file_path.replace('.txt', '_message.txt')

sql_list = []
current_date_time = datetime.now()

def get_sql_message_list():
    message_list = []
    index = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()

            if not line:
                break

            index = index + 1
            match = re.compile(r'view_text=\'(.*?)\'.*?resource_key=\'(.*?)\'').findall(line)
            if match:
                info = match[0]
                message_list.append({
                    'key': info[1],
                    'message_cn': info[0],
                    'message_en': None,
                    'sql': False
                })

    with open(message_file_path, 'w', encoding='utf-8') as file:
        json.dump(message_list, file, indent=4, ensure_ascii=False)


def translate_message_list():
    with open(message_file_path, 'r', encoding='utf-8') as file:
        message_list = json.load(file)

    no_en_message_list = list(filter(lambda x: x['message_en'] is None or x['message_en'] == '', message_list))
    print(len(no_en_message_list))

    no_en_message_group = []
    group_count = math.ceil(len(no_en_message_list) / len(baidu_api_info_list))

    for i in range(0, len(no_en_message_list), group_count):
        no_en_message_group.append(no_en_message_list[i:i + group_count])

    task_list = []
    index = 0

    for group in no_en_message_group:
        baidu_api_info = baidu_api_info_list[index]
        task_list.append(threading.Thread(target=translate_message_group, args=(group, baidu_api_info, index + 1)))
        index = index + 1

    task_list.append(threading.Thread(target=write_message_file, args=(message_list,)))

    for task in task_list:
        task.start()

    for task in task_list:
        task.join()


def translate_message_group(message_list, baidu_api_info, index):
    total_count = len(message_list)
    count = 0
    error_count = 0
    for message in message_list:
        if message['message_en'] is None or message['message_en'] == '':
            if error_count >= 5:
                break

            try:
                count = count + 1
                message['message_en'] = translate_message(message['message_cn'], baidu_api_info)
                message['sql'] = r"update sys_message_resource set view_text='%s' where resource_key='%s' and language_type = 'en-us';" % (message['message_en'].replace("\'", "''"), message['key'])
                print(str(index) + ':' + str(count) + '|' + str(total_count))
            except Exception as error:
                error_count = error_count + 1
                pass


def write_message_file(message_list):
    in_date_time = datetime.now()
    while True:
        execute_date_time = datetime.now()

        if (execute_date_time - in_date_time).seconds >= 60:
            with open(message_file_path, 'w', encoding='utf-8') as file:
                json.dump(message_list, file, indent=4, ensure_ascii=False)

            in_date_time = datetime.now()


def read_message_file():
    result = []
    if os.path.exists(message_file_path):
        with open(message_file_path, 'r', encoding='utf-8') as file:
            result = json.load(file)
    return result


def write_new_sql_file(new_message_sql_list):
    with open(file_path.replace('.txt', '_new.txt'), 'w', encoding='utf-8') as file:
        for sql in new_message_sql_list:
            file.write(sql)
            file.write('\n')


new_message_list = read_message_file()
new_message_sql_list = [].extend([message['sql'] for message in new_message_list])

write_new_sql_file(new_message_sql_list)
