import os
import concurrent.futures

from modules.service.movie.video.video_file import VideoFile
from modules.service.movie.video.video_folder import VideoFolder

from modules.service.movie.neaten.porter import Porter


class Collator(object):
    def __init__(self):
        pass

    def run_by_paths(self, paths: list):
        videos = self.__build_video__(paths)
        self.__run__(videos)

    def run_by_path(self, path: str):
        videos = self.__build_video__([os.path.join(path, item) for item in os.listdir(path)])
        self.__run__(videos)

    def __build_video__(self, paths: list):
        videos = []

        for path in paths:
            if os.path.isdir(path):
                videos.append(VideoFolder(path))
            else:
                videos.append(VideoFile(path))

        return videos

    def __run__(self, videos: list):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.__neaten__, videos)

    def __neaten__(self, video):
        Porter(video).work()
