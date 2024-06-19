from modules.service.movie_cut.butcher import Butcher

path_params = [
    r"/Users/vito/Movies/教学/move/ABF-087.mp4"
]

for path in path_params:
    if path is not None and path != '':
        Butcher(path).chop()

print("Done")
