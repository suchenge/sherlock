from modules.service.movie.clip.editor import Editor

path_params = [
    r"/Users/vito/Movies/教学/move/NSFS-308.mp4"
]

Editor(path_params).cut()

print("Done")
