import concurrent.futures

from modules.tools.common_methods.unity_tools import get_file_suffix
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

    def __download__(self, image):
        image['executor'](**image)

    def download(self):
        resolver = Resolver(self.__url__)
        title = resolver.get_title()
        images = resolver.get_images()

        save_folder = f'{self.__save_path__}/{title}'
        save_images = []

        for index in range(len(images)):
            image = images[index]
            is_dict = isinstance(image, dict)

            if is_dict:
                image_url = image['url']
                image_path = f"{save_folder}/{image['name']}"
            else:
                image_url = image
                image_path = f'{save_folder}/{str(index).zfill(5)}.{get_file_suffix(image_url)}'

            save_images.append({'path': image_path, 'url': image_url, 'executor': resolver.download_images})

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.__download__, save_images)

