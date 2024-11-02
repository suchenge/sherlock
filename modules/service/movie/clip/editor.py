import os
import uuid

from ffmpy import FFmpeg

from modules.tools.common_methods.unity_tools import ffmpeg_execute_path

from modules.service.movie.clip.clip_file import ClipFile
from modules.service.movie.video.video_file import VideoFile
from modules.service.movie.video.video_folder import VideoFolder

class Editor(object):
    def __init__(self, paths: list[str]):
        self.__videos__ = []
        self.__ffmpeg_path__ = ffmpeg_execute_path()

        for path in paths:
            if os.path.exists(path) is False:
                continue

            if os.path.isfile(path):
                file = VideoFile(path)

                if file.is_movie:
                    self.__videos__.append(VideoFile(path))
            else:
                self.__videos__.extend(VideoFolder(path).files)

    def merge(self):
        video_files = filter(lambda x: x.is_movie, self.__videos__)
        video_file_paths = sorted(video_files, key=lambda x: x.name)

        first_video = self.__videos__[0]

        merge_time_line_file_path = f'{first_video.parent}/{uuid.uuid4().hex}.txt'
        merge_file_name = first_video.name.replace(first_video.type, '')
        merge_file_path = f'{first_video.parent}/{merge_file_name}merge.{first_video.type}'

        with open(merge_time_line_file_path, 'w', encoding='utf') as merge_file:
            for video_file in video_file_paths:
                merge_file.write(f'file \'{video_file.path}\'\r\n')

        try:
            FFmpeg(
                    global_options=['-f', 'concat'],
                    inputs={merge_time_line_file_path: ['-safe', '0']},
                    outputs={merge_file_path: ['-c', 'copy']},
                    executable=self.__ffmpeg_path__
                ).run()
        except Exception as error:
            print(error)
        finally:
            os.remove(merge_time_line_file_path)

    def cut(self):
        for video in self.__videos__:
            clip_file = ClipFile(video)

            if clip_file.is_usable:

                print(f'剪辑文件{clip_file.__path__}开始')
                clip_file.cut()

                if clip_file.need_merge:
                    print(f'自动合并剪辑文件')
                    clip_file.merge()

                print(f'剪辑文件{clip_file.__path__}完成')


