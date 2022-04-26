import os
import sys

cur_path = os.path.abspath(os.path.dirname(__file__))
module_path = os.path.split(cur_path)[0]
sys.path.append(module_path)

from modules.av.collate.collator import Collator

# os.system("pause")
Collator(sys.argv[1]).run()


