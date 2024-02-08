import os
import concurrent.futures

from modules.tools.http_request.http_client import HttpClient
from modules.service.download.picture.resolver import Resolver


class Processor(object):
    def __init__(self, url, save_path):
        self.__url__ = url
        self.__save_path__ = save_path
        self.__title__ = None
        self.__images__ = []

    @property
    def url(self):
        return self.__url__

    def __get_picture_suffix__(self, image_url):
        picture_name = os.path.split(image_url)[-1]
        picture_suffix = picture_name.split(".")[-1]
        return picture_suffix

    def __download__(self, image):
        HttpClient.download(**image)

    def download(self):
        resolver = Resolver(self.__url__)
        title = resolver.get_title()
        images = resolver.get_images()

        save_folder = f'{self.__save_path__}/{title}'
        save_images = []

        for index in range(len(images)):
            save_images.append({
                'path': f'{save_folder}/{str(index).zfill(5)}.{self.__get_picture_suffix__(images[index])}',
                'url': images[index]
            })

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.__download__, save_images)

