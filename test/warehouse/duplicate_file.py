import json
import os
import re
import shutil

import modules.tools.common_methods.unity_tools as unity_tools

warehouse_reference_path = r"D:\warehouse"

warehouse_paths = [
    {
        "driver": "G",
        "paths": [
            r"G:\传输\describe",
            r"G:\传输\javdb"
        ]
    },
    {
        "driver": "Seagate Expansion Drive",
        "paths": [
            r"H:\教学\编程\move\AV"
        ]
    },
    {
        "driver": "4T.Temp.2017",
        "paths": [
            r"H:\无码",
            r"H:\无码",
            r"H:\有码",
        ]
    },
    {
        "driver": "8T.Save.2023",
        "paths": [
            r"J:\New\视频\Temp",
            r"J:\New\视频\VR",
            r"J:\New\视频\写真",
            r"J:\New\视频\有码",
            r"J:\Save\视频\VR",
            r"J:\Save\视频\写真",
            r"J:\Save\视频\有码",
        ]
    },
    {
        "driver": "4T.Save.2018",
        "paths": [
            r"K:\Temp",
            r"K:\写真",
            r"K:\有码"
        ]
    },
    {
        "driver": "4T.Temp.2019",
        "paths": [
            r"M:\写真",
            r"M:\有码",
        ]
    },
    {
        "driver": "4T.Temp.2021",
        "paths": [
            r"N:\Temp\视频\AV",
        ]
    }
]

def build_warehouse_item_id(item_id):
    result = item_id.split(" ")[0]

    match = re.search(r'^\d+(.*?)', result)
    if match:
        result = result.replace(match.group(0), '')

    return result

def build_warehouse_item(file_item, parent_path):
    files = []

    file_item_path = os.path.join(parent_path, file_item)
    is_file = os.path.isfile(file_item_path)

    if is_file:
        file_name, file_extension = os.path.splitext(file_item)
        item_id = file_name
        files.append({
            "name": file_item,
            "size": os.path.getsize(file_item_path)
        })
    else:
        item_id = file_item
        for item in os.listdir(file_item_path):
            item_path = os.path.join(file_item_path, item)
            if unity_tools.is_movie_file(item_path):
                files.append({
                    "name": item,
                    "size": os.path.getsize(item_path)
                })

    item_id = build_warehouse_item_id(item_id)

    return {
        "name": file_item,
        "path": file_item_path,
        "is_file": is_file,
        "id": item_id,
        "files": files
    }

def build_warehouse_reference():
    reference_paths = []
    for warehouse_path in warehouse_paths:
        references = []

        for path in warehouse_path["paths"]:
            if os.path.exists(path) is False:
                continue

            index = 0
            for item in os.listdir(path):
                index += 1
                reference = build_warehouse_item(item, path)
                reference["index"] = index
                references.append(reference)

        reference_path = os.path.join(warehouse_reference_path, f'{warehouse_path["driver"]}.json')
        reference_content = json.dumps(references, sort_keys=True, indent=4, ensure_ascii=False)
        reference_paths.append(reference_path)

        if os.path.exists(reference_path):
            os.remove(reference_path)

        with open(reference_path, "w", encoding="utf-8") as file:
            file.write(reference_content)

    warehouse_reference_file_path = os.path.join(warehouse_reference_path, "warehouse_reference.json")

    if os.path.exists(warehouse_reference_file_path):
        warehouse_reference = json.load(open(warehouse_reference_file_path, "r", encoding="utf-8"))
        for warehouse_reference_item in warehouse_reference:
            if warehouse_reference_item not in reference_paths:
                reference_paths.append(warehouse_reference_item)

    with open(warehouse_reference_file_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(reference_paths, sort_keys=True, indent=4, ensure_ascii=False))


def build_duplicate_reference():
    warehouse_reference_paths = os.path.join(warehouse_reference_path, "warehouse_reference.json")
    duplicate_reference_path = os.path.join(warehouse_reference_path, "warehouse_duplicate_reference.json")
    reference_paths = json.load(open(warehouse_reference_paths, 'r', encoding="utf-8"))
    warehouses = {}

    if os.path.exists(duplicate_reference_path):
        warehouses = json.load(open(duplicate_reference_path, 'r', encoding="utf-8"))

    for reference_path in reference_paths:
        reference = json.load(open(reference_path, 'r', encoding="utf-8"))
        reference_name = os.path.basename(os.path.normpath(reference_path))
        driver, ext = os.path.splitext(reference_name)

        for reference_item in reference:
            reference_id = reference_item["id"]
            warehouse_id = warehouses.get(reference_id)
            warehouse_info = {"files": reference_item["files"], "path": reference_item["path"], "driver": driver}
            if warehouse_id is None:
                warehouses[reference_id] = [warehouse_info]
            else:
                if warehouse_info["driver"] not in [item["driver"] for item in warehouses[reference_id]]:
                    warehouses[reference_id].append(warehouse_info)

    duplicate_references = {}
    for warehouse in warehouses:
        warehouse_reference = warehouses[warehouse]

        if len(warehouse_reference) > 1:
            duplicate_references[warehouse] = warehouse_reference

    if os.path.exists(duplicate_reference_path):
        os.remove(duplicate_reference_path)

    with open(duplicate_reference_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(duplicate_references, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    build_warehouse_reference()
    build_duplicate_reference()
