import json
import os
from modules.service.movie_warehouse.collate.file import File

dict_path = "D:\\dictionary\\indexs\\"
es_path = "D:\\tools\\Everything-Command\\es.exe"


def add(file_info: File):
    file_path = dict_path + file_info.name + ".json"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        json_object = json.loads(content)
        if file_info.path in json_object["paths"]:
            json_object["paths"].append(file_info.path)
    else:
        json_object = {"sn": file_info.name, "paths": [file_info.path]}

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(json_object, sort_keys=True, indent=4, ensure_ascii=False))


def exists(file_info: File):
    file_path = dict_path + file_info.name + ".json"
    json_exists = os.path.exists(file_path)
    if json_exists:
        print("%s exists %s" % (file_info.name, file_path))
        return True
    else:
        es_result = search(file_info.name)
        for es_path, es_filename in es_result:
            if file_info.path not in es_path and file_info.title in es_path and file_info.name in es_filename:
                print("%s exists %s" % (file_info.name, es_path))
                return True

        return False


def search(keyword):
    result = []

    if os.path.exists(es_path):
        es_search = os.popen(es_path + " " + keyword)

        for line in es_search.readlines():
            file_info = os.path.split(line.replace("\n", "").replace("\r", ""))
            path, filename = file_info[0], file_info[1]
            result.append((path, filename))

    return result

