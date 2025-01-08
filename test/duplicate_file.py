import json
import os

warehouse_reference_path = r"D:\tools"

warehouse_paths = [
    {
        "driver": "E",
        "paths": [
            r"E:\Music\歌曲",
            r"E:\Music\讲座"
        ]
    }
]

def build_warehouse_reference():
    reference_paths = []
    for warehouse_path in warehouse_paths:
        references = []

        for path in warehouse_path["paths"]:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                is_file = os.path.isfile(item_path)
                item_id = item

                item_id = item.split(" ")[0]
                if is_file is True:
                    item_id = item_id.split(".")[0]

                reference = {
                    "name": item,
                    "path": item_path,
                    "is_file": is_file,
                    "id": item_id
                }

                references.append(reference)

        reference_path = os.path.join(warehouse_reference_path, f'{warehouse_path["driver"]}.json')
        reference_content = json.dumps(references, sort_keys=True, indent=4, ensure_ascii=False)
        reference_paths.append(reference_path)

        if os.path.exists(reference_path):
            os.remove(reference_path)

        with open(reference_path, "w", encoding="utf-8") as file:
            file.write(reference_content)

    with open(os.path.join(warehouse_reference_path, "warehouse_reference.json"), "w", encoding="utf-8") as file:
        file.write(json.dumps(reference_paths, sort_keys=True, indent=4, ensure_ascii=False))


def build_duplicate_reference():
    warehouse_reference_paths = os.path.join(warehouse_reference_path, "warehouse_reference.json")
    duplicate_reference_path = os.path.join(warehouse_reference_path, "duplicate_reference.json")
    reference_paths = json.load(open(warehouse_reference_paths, 'r', encoding="utf-8"))
    warehouses = {}

    for reference_path in reference_paths:
        reference = json.load(open(reference_path, 'r', encoding="utf-8"))

        for reference_item in reference:
            reference_id = reference_item["id"]
            warehouse_id = warehouses.get(reference_id)
            if warehouse_id is None:
                warehouses[reference_id] = [reference_item["path"]]
            else:
                warehouses[reference_id].append(reference_item["path"])

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
