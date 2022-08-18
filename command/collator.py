import os
import sys


os.system("pause")
cur_path = os.path.abspath(os.path.dirname(__file__))
module_path = os.path.split(cur_path)[0]
sys.path.append(module_path)

from modules.service.movie_warehouse.collate.collator import Collator

Collator(sys.argv[1]).run()



