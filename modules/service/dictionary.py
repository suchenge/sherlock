import json
import os

dict_path = "D:\\dictionary\\indexs\\"
es_path = "D:\\tools\\Everything-Command\\es.exe"


def add(uid, filename):
    file_path = dict_path + uid + ".json"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        json_object = json.loads(content)
        if filename in json_object["paths"]:
            json_object["paths"].append(filename)
    else:
        json_object = {"sn": uid, "paths": [filename]}

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(json_object, sort_keys=True, indent=4, ensure_ascii=False))


def exists(uid, current_path=None):
    file_path = dict_path + uid + ".json"
    json_exists = os.path.exists(file_path)
    if json_exists:
        return True
    else:
        if current_path is not None:
            es_result = search(uid)
        return True


def search(keyword):
    result = []

    if os.path.exists(es_path):
        es_search = os.popen(es_path + " " + keyword)

        for line in es_search.readlines():
            file_info = os.path.split(line.replace("\n", "").replace("\r", ""))
            path, filename = file_info[0], file_info[1]
            result.append((path, filename))

    return result

