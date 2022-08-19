import os
import sys

# os.system("pause")

cur_path = os.path.abspath(os.path.dirname(__file__))
module_path = os.path.split(cur_path)[0]
sys.path.append(module_path)

from modules.service.movie_warehouse.collate.collator import Collator
from modules.tools.exception_container.exception_list import ExceptionList

collator = Collator(sys.argv[1])
collator.run()

exception_container = ExceptionList()

if exception_container.empty() is False:
    exception_container.print()
    os.system("pause")
