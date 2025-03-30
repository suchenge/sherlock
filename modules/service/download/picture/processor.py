import concurrent.futures

from modules.service.download.picture.strategy.provider import ResolverStrategyProvider


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

        resolver = ResolverStrategyProvider.get_strategy(self.__url__)

        title = resolver.get_title()
        print(f'解析到title:{title}')

        images = resolver.get_images()
        print(f'解析到图片：{str(len(images))}条')

        save_folder = f'{self.__save_path__}/{title}'
        save_images = [
                        {
                            'path': f"{save_folder}/{item.file_name}",
                            'url': item.url,
                            'executor': resolver.download_image
                        }
                        for item in images
                      ]

        print("开始下载解析到的所有图片")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.__download__, save_images)

            success_result = [result for result in results if result is not None]
            error_results = [result for result in results if result is None]

            print(f'下载图片完成，成功{str(len(success_result))}条，失败{(str(len(error_results)))}条')

            if len(error_results) > 0:
                raise Exception(f'含有下载出错的记录')
