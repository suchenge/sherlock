import os
import json
import shutil

warehouse_reference_path = r"D:\warehouse\warehouse_torrent_group.json"

torrent_reference_paths = [
    r"G:\传输\种子\000.save",
    r"G:\传输\种子\001.waiting for download",
    r"G:\传输\种子\002.need to look at",
]

def build_torrent_reference():
    torrent_references = {}
    for torrent_reference_path in torrent_reference_paths:
        for reference_path in os.listdir(torrent_reference_path):
            reference_id = reference_path.split(" ")[0]
            reference_path = os.path.join(torrent_reference_path, reference_path)

            torrent_reference = torrent_references.get(reference_id)
            if torrent_reference is None:
                torrent_references[reference_id] = reference_path
            else:
                shutil.rmtree(reference_path)

    if os.path.exists(warehouse_reference_path):
        os.remove(warehouse_reference_path)

    with open(warehouse_reference_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(torrent_references, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    build_torrent_reference()
