import os
import re
import shutil
from itertools import groupby
from pathlib import Path

file_path = "E:\Temp\Done\漫画"
files = []
file_group = []

for file_name in os.listdir(file_path):
    item_file_path = os.path.join(file_path, file_name)
    if os.path.isfile(item_file_path) and file_name.endswith(".epub"):

        try:
            title = re.compile('\[.*?\]\[(.*?)\].*?\.epub', re.DOTALL).search(file_name).group(1)

            if title is not None and title != '':
                file = {
                    "name": file_name,
                    "path": item_file_path,
                    "title": title
                }

                files.append(file)
        except:
            print(file_name)

for key, group in groupby(files, lambda file: file["title"]):
    file_group.append({
        "key": key,
        "files": list(group)
    })

for group in file_group:
    group_file = group["files"]
    group_key = group["key"]
    file_count = len(group_file)

    if file_count > 1:
        group_path = os.path.join(file_path, group_key)

        if os.path.exists(group_path) is False:
            Path(group_path).mkdir(exist_ok=True)

        for item in group_file:
            source_file_path = item["path"]
            target_file_path = os.path.join(group_path, item["name"])
            shutil.move(source_file_path, target_file_path)
