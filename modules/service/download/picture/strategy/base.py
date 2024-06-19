import os

from urllib.parse import urlparse


class Base(object):
    def __init__(self, url, html):
        self.__url__ = url
        self.__html__ = html
        self.__domain_url__, self.__url_path__ = self.__parse_url__()

    @staticmethod
    def is_match(url, html):
        return False

    def __parse_url__(self):
        url_info = urlparse(self.__url__)
        return url_info.scheme + "://" + url_info.netloc, url_info.path

    def __get_picture_suffix__(self, image_url):
        picture_name = os.path.split(image_url)[-1]
        picture_suffix = picture_name.split(".")[-1]

        if picture_suffix == 'webp':
            picture_suffix = 'jpg'

        return picture_suffix

    def get_title(self):
        return None

    def get_child_page_url(self):
        return []

    def get_images(self, html, page_index=None):
        return []
