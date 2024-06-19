import concurrent.futures

from lxml import etree
from urllib.parse import urlparse

from modules.tools.http_request.http_client import HttpClient

from modules.service.download.picture.strategy.provider import ResolverStrategyProvider


class Resolver(object):
    def __init__(self, url):
        self.__url__ = url

        self.__domain_url__, self.__url_path__ = self.__parse_url__()

        self.__html__ = self.__get_page_html_tree__(self.__url__)
        self.__strategy__ = ResolverStrategyProvider.get_strategy(self.__url__, self.__html__)

    def __parse_url__(self):
        url_info = urlparse(self.__url__)
        return url_info.scheme + "://" + url_info.netloc, url_info.path

    def __get_page_html_tree__(self, url):
        html = HttpClient.get_text(url)
        return etree.HTML(html)

    def __get_child_page_url__(self):
        return self.__strategy__.get_child_page_url()

    def __get_page_images__(self, page):
        page_index = None
        page_url = None

        if isinstance(page, dict):
            page_url = page['url']
            page_index = page['index']
        else:
            page_url = page

        html = self.__get_page_html_tree__(page_url)
        return self.__strategy__.get_images(html, page_index)

    def __get_images__(self):
        urls = self.__get_child_page_url__()
        result = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            page_images = executor.map(self.__get_page_images__, urls)

            for images in page_images:
                for image in images:
                    result.append(image)

        return result

    def get_title(self):
        return self.__strategy__.get_title()

    def get_images(self):
        return self.__get_images__()
