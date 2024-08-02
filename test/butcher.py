import os
from ffmpy import FFmpeg

from modules.service.movie_cut.butcher import Butcher
from modules.tools.common_methods.unity_tools import ffmpeg_execute_path

path_params = [
    r"/Users/vito/Movies/教学/move/20240515-VIP.mp4"
]


# 文件合并
'''
menu_file_path = r'/Users/vito/Movies/教学/move/20240515-VIP.txt'
concat_file = os.path.join('/Users/vito/Movies/教学/move', '20240515-VIP.txt')
ff = FFmpeg(
    global_options=['-f', 'concat'],
    inputs={concat_file: ['-safe', '0']},
    outputs={path_params[0] : ['-c', 'copy']},
    executable = ffmpeg_execute_path()
)

print(ff.cmd)

ff.run()
'''

for path in path_params:
    if path is not None and path != '':
        Butcher(path).chop()

print("Done")
