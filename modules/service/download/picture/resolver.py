import concurrent.futures

from modules.tools.common_methods.unity_tools import parse_url, format_title

from modules.service.download.picture.strategy.provider import ResolverStrategyProvider


class Resolver(object):
    def __init__(self, url):
        self.__url__ = url

        self.__domain_url__, self.__url_path__ = parse_url(url)
        self.__strategy__ = ResolverStrategyProvider.get_strategy(self.__url__)

    def __get_page_images__(self, page):
        page_index = None
        page_url = None

        if isinstance(page, dict):
            page_url = page['url']
            page_index = page['index']
        else:
            page_url = page

        if page_url == self.__url__:
            html = self.__strategy__.html
        else:
            html = self.__strategy__.get_tree(page_url)

        images = self.__strategy__.get_images(html, page_index)
        return images

    def __get_images__(self):
        urls = self.__strategy__.get_child_page_url()
        result = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            page_images = executor.map(self.__get_page_images__, urls)

            for images in page_images:
                for image in images:
                    result.append(image)

        return result

    def get_title(self):
        title = self.__strategy__.get_title()
        return format_title(title)

    def get_images(self):
        return self.__get_images__()

    def download_image(self, **images):
        self.__strategy__.download_image(**images)
