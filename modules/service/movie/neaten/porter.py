import os
import shutil
import concurrent.futures

from pathlib import Path

from modules.service.movie.analysis.analyst import Analyst

from modules.service.movie.video.video_folder import VideoFolder
from modules.service.movie.video.video_path import VideoPath


class Porter(object):
    def __init__(self, video: VideoPath):
        self.__video__ = video
        self.__analyst__ = None
        self.__information__ = None

    def work(self):
        self.__analyst__ = Analyst(self.__video__.uid)
        self.__information__ = self.__analyst__.get_information()

        video_name = f'{self.__video__.uid} {self.__information__.title}'
        video_path = os.path.join(self.__video__.parent, video_name)

        if isinstance(self.__video__, VideoFolder):
            os.rename(self.__video__.path, video_path)
        else:
            Path(video_path).mkdir(exist_ok=True)
            shutil.move(self.__video__.path, os.path.join(video_path, self.__video__.name))

        images = self.__build_images__(video_path)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.__download_image__, images)

    def __build_images__(self, save_path):
        images = [self.__build_image__(self.__information__.poster, save_path)]

        index = 1
        for image in self.__information__.stills:
            images.append(self.__build_image__(image, save_path, index))
            index += 1

        return images

    def __build_image__(self, url, save_path, index=None):
        file_type = url.split('.')[-1]
        name = self.__video__.uid

        if index is not None:
            name = f'{name}_{str(index).zfill(3)}'

        name = f'{name}.{file_type}'
        return {
            "path": os.path.join(save_path, name),
            "url": url
        }

    def __download_image__(self, image):
        self.__analyst__.request.download(**image)

