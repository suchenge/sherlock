import os
import sys

# os.system("pause")
cur_path = os.path.abspath(os.path.dirname(__file__))
module_path = os.path.split(cur_path)[0]
sys.path.append(module_path)


from modules.service.movie.neaten.collator import Collator

collator = Collator()
collator.run_by_paths([sys.argv[1]])
