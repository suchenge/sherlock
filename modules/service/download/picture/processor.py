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
        return image['executor'](**image)

    def download(self):
        print(f'解析地址：{self.__url__}')

        resolver = Resolver(self.__url__)

        title = resolver.get_title()
        print(f'解析到title:{title}')

        images = resolver.get_images()
        print(f'解析到图片：{str(len(images))}条')

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

            save_images.append({'path': image_path, 'url': image_url, 'executor': resolver.download_image})

        print("开始下载解析到的所有图片")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.__download__, save_images)

            success_result = [result for result in results if result is True]
            error_results = [result for result in results if result is False]

            print(f'下载图片完成，成功{str(len(success_result))}条，失败{(str(len(error_results)))}条')

            if len(error_results) > 0:
                raise Exception(f'含有下载出错')
