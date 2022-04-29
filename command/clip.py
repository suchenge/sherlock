import os
import sys

cur_path = os.path.abspath(os.path.dirname(__file__))
module_path = os.path.split(cur_path)[0]
sys.path.append(module_path)

from modules.movie_cut.butcher import Butcher

os.system("pause")

path_param = sys.argv[1]
func = lambda path: Butcher(path).chop()

if isinstance(path_param, str):
    func(path_param)
else:
    for path in path_param:
        func(path)
