import os
import sys

cur_path = os.path.abspath(os.path.dirname(__file__))
module_path = os.path.split(cur_path)[0]
sys.path.append(module_path)

from modules.av.collate.collator import FileType, Collator

print(sys.argv[0])
paths = sys.argv[1]
file_type = sys.argv[2]

if file_type == FileType.DIR:
    print("处理当前目录 " + paths)
else:
    print("处理所选文件:" + paths)

Collator(paths, FileType[file_type]).run()

