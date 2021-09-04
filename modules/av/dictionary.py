import json
import os

dict_path = "D:\\dictionary\\indexs\\"


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

    print("写入字典")
