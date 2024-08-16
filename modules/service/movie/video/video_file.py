import os

from modules.service.movie.video.video_path import VideoPath


class VideoFile(VideoPath):
    def __init__(self, path):
        super().__init__(path)

    @property
    def is_movie(self):
        types = ['mkv', 'mp4', 'avi', 'wmv']
        if self.__type__.lower() in types:
            return True
        else:
            return False
