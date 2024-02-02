from modules.service.movie_cut.butcher import Butcher

path_params = [
    r"/Users/vito/Movies/剧集/test_move_cute/01.mp4"
]

for path in path_params:
    if path is not None and path is not '':
        Butcher(path).chop()

print("Done")
