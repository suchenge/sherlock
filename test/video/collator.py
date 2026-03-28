from modules.service.movie.neaten.collator import Collator

paths = [
    r'/Users/vito/Movies/AV/VDD-200.mp4',
]

collator = Collator()
collator.run_by_paths(paths)

# collator.run_by_path(r'E:\临时文件')


