import os

from modules.service.movie.clip.clip_file import ClipFile
from modules.service.movie.video.video_file import VideoFile
from modules.service.movie.video.video_folder import VideoFolder

class Editor(object):
    def __init__(self, paths: list[str]):
        self.__videos__ = []

        for path in paths:
            if os.path.exists(path) is False:
                continue

            if os.path.isfile(path):
                file = VideoFile(path)

                if file.is_movie:
                    self.__videos__.append(VideoFile(path))
            else:
                self.__videos__.extend(VideoFolder(path).files)

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


