import os

from modules.service.movie.video.video_file import VideoFile
from modules.service.movie.video.video_path import VideoPath


class VideoFolder(VideoPath):
    def __init__(self, path):
        super().__init__(path)
        self.__files__ = [VideoFile(os.path.join(path, file_name)) for file_name in os.listdir(path)]
        self.__files__ = filter(lambda file: file.is_movie, self.__files__)

    @property
    def files(self):
        return self.__files__
