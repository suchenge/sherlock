import os

from lxml import etree
from urllib.parse import urlparse

from modules.tools.http_request.http_client import HttpClient


class BaseCartoonStrategy(object):
    def __init__(self, url):
        self.__url__ = url
        html = HttpClient.get_text(url)
        self.__html__ = etree.HTML(html)

    @staticmethod
    def is_match(url):
        return False

    def __parse_url__(self):
        url_info = urlparse(self.__url__)
        return url_info.scheme + "://" + url_info.netloc, url_info.path

    def get_title(self):
        return None

    def get_image(self):
        return []
