import json
import os
import os.path

t_msg_sql_file_path = r'E:\Download\T_Msg.sql'

def collating_t_message():
    msg_sql_list = []
    with open(t_msg_sql_file_path, 'r', encoding='utf-8') as file:
        sql_list = file.readlines()
        for sql in sql_list:
            count = sql.count(';')
            if count > 1:
                temp_sql_list = sql.split(';')
                for temp_sql in temp_sql_list:
                    msg_sql_list.append(temp_sql + ";\n")
            else:
                msg_sql_list.append(sql)

    with open(t_msg_sql_file_path, 'w', encoding='utf-8') as file:
        file.writelines(msg_sql_list)


def get_message_info(message_file_path):
    with open(message_file_path, 'r', encoding='utf-8') as file:
        file_info = json.load(file)
        message_list = {}

        for message_info in file_info['message_info_list']:
            message = message_info["message"]
            key = message_info["new_key"] if message_info.get("new_key") and message_info["new_key"] else message_info["exists_key"]

            if message not in message_list:
                message_list[message] = key

        return {
            "file_path": file_info["file_path"],
            "message_list": message_list,
            "sql_list": file_info["new_message_key_sql"]
        }


def file_message_replace(message_file_name):
    if '.json' not in message_file_name:
        message_file_name = message_file_name + '.json'

    message_file_path = os.path.join('E:\\Download\\', message_file_name)
    message_info = get_message_info(message_file_path)

    file_content = ''
    with open(message_info['file_path'], 'r', encoding='utf-8') as file:
        file_content = file.read()

    for message in message_info["message_list"]:
        print(message)
        key = message_info["message_list"][message]

        if key in file_content:
            break

        old_message = '"%s"' % message
        new_message = '%s, "%s"' % (old_message, key)
        file_content = file_content.replace(old_message, new_message)

    with open(message_info['file_path'], 'w', encoding='utf-8') as file:
        file.write(file_content)

    with open(t_msg_sql_file_path, 'a', encoding='utf-8') as file:
        for sql in message_info['sql_list']:
            file.write(sql)
            file.write("\n")

    os.rename(message_file_path, message_file_path.replace('pending-', 'done-'))

    print(message_info['file_path'])

def get_message_next_file_path():
    dir_name = r'E:\\Download\\'
    file_list = [l for l in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, l)) and 'pending-' in l and '-message.json' in l]
    print (len(file_list))
    return file_list[0]

message_file_path = r'pending-DeletePurchaseOrderByExternalOrderId-message'
message_file_path = get_message_next_file_path()
file_message_replace(message_file_path)
# collating_t_message()

