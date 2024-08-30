from modules.service.movie.neaten.collator import Collator

paths = [
    r'/Users/vito/Movies/教学/temp/MBRBA-116.mp4',
    r'/Users/vito/Movies/教学/temp/MBRBA-101.mp4',
    r'/Users/vito/Movies/教学/temp/MBRBA-108.mp4',
    r'/Users/vito/Movies/教学/temp/MBRBA-110.mp4',
    r'/Users/vito/Movies/教学/temp/MBRBA-112.mp4',
]

collator = Collator()
collator.run_by_paths(paths)

# collator.run_by_path(r'E:\临时文件')


