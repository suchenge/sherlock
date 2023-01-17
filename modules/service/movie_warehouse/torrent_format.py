import os
import re
from modules.service import \
    dictionary

path = 'G:\\种子\\002'


def __file_info__(file_name):
    source_path = os.path.join(path, file_name)

    file_size = os.stat(source_path).st_size
    file_type = file_name.split('.')[-1]
    file_title = file_name.replace(file_type, '').strip('.').upper()

    i = file_title.rfind('@')
    if i >= 0:
        file_title = file_title[i + 1: len(file_title) + 1]

    file_title = file_title.replace('FHD_6M-', '')

    if '-' not in file_title:
        match = re.compile(r'(\d+)').findall(file_title)
        if match:
            file_title = file_title.replace(match[0], '-' + match[0])

    target_path = os.path.join(path, file_title + '.' + file_type)

    return file_title, file_size, source_path, target_path


files = [__file_info__(file_name) for file_name in os.listdir(path)]

for title, size, source_path, target_path in files:
    if dictionary.exists(title):
        os.remove(source_path)
        continue

    if os.path.exists(target_path):
        if os.stat(target_path).st_size >= size:
            os.remove(source_path)
            continue
        else:
            os.remove(target_path)

    os.rename(source_path, target_path)
