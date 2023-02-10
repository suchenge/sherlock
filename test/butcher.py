from modules.service.movie_cut.butcher import Butcher

path_params = [
    r""
    , r""
    , r""
    , r""
    , r""
    , r""
    , r""
    , r""
    , r""
    , r""
    , r""
]

for path in path_params:
    if path is not None and path is not '':
        Butcher(path).chop()

print("Done")
