import time
import requests
import random
import re
import pymysql

t_msg_sql_file_path = r'E:\Download\T_Msg.sql'

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


def get_database_message_key(sql):
    result = {}
    database_cursor = database_connect.cursor()
    database_cursor.execute(sql)
    database_result = database_cursor.fetchall()

    if len(database_result) <= 0:
        return []

    for row in database_result:
        key = row[0]
        text_cn = row[1]
        text_en = row[2]

        if key not in result:
            result[key] = {}

        result[key] = {
            'zh_cn': text_cn,
            'en_us': text_en
        }

    return result


def get_vito_temp_message_sql_list():
    query_temp_sys_message_resource_sql = 'SELECT `Key`, VIEW_TEXT_CH, VIEW_TEXT_EN FROM vito_temp_sys_message_resource'
    return get_database_message_key(query_temp_sys_message_resource_sql)

    '''
    result.append("CALL T_MSG('%s','%s','%s');" % (message_info["key"], message_info["text_cn"], 'zh_cn'))
    result.append("CALL T_MSG('%s','%s','%s');" % (message_info["key"], message_info["text_en"], 'en_us'))
    '''


def get_t_msg_file_sql_list():
    result = {}
    with open(t_msg_sql_file_path, 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()
            if not line:
                break

            regex_line = r'CALL T_MSG\(\'(.*?)\',\'(.*?)\',\'(.*?)\'\);'
            reg_match = re.compile(regex_line).findall(line)

            if reg_match and len(reg_match) > 0:
                key = reg_match[0][0]
                text = reg_match[0][1]
                message_type = reg_match[0][2]

                if key not in result:
                    result[key] = {}

                result[key][message_type] = text

    return result


def merge():
    file_message_list = get_t_msg_file_sql_list()
    database_message_list = get_vito_temp_message_sql_list()

    for key in database_message_list:
        if key in file_message_list:
            database_message_list[key] = file_message_list[key]

    for key in file_message_list:
        if key not in database_message_list:
            database_message_list[key] = file_message_list[key]

    merged_message_list = sorted(database_message_list.items(), reverse=False)

    with open(t_msg_sql_file_path.replace('.sql', '_new.sql'), 'w', encoding='utf-8') as file:
        for message_info in merged_message_list:
            key = message_info[0]
            message = message_info[1]

            if 'Center_' in key:
                file.write("CALL T_MSG('%s','%s','%s');" % (key, message["zh_cn"], 'zh_cn'))
                file.write('\n')
                file.write("CALL T_MSG('%s','%s','%s');" % (key, message["en_us"], 'en_us'))
                file.write('\n')

                file.write('\n')


merge()

