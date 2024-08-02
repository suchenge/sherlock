import os

from pathlib import Path
from lxml import etree

from modules.tools.common_methods.unity_tools import parse_url
from modules.tools.http_request.request import Request

class Base(object):
    def __init__(self, url):
        self.__url__ = url
        self.__domain_url__, self.__url_path__ = parse_url(url)
        self.__request__ = self.__get_request__()
        self.__html__ = self.get_tree(url)

    @staticmethod
    def is_match(url):
        return False

    @property
    def html(self):
        return self.__html__

    def __get_request__(self):
        return Request()

    def get_title(self):
        return None

    def get_child_page_url(self):
        return []

    def get_images(self, html, page_index=None):
        return []

    def get_html(self, url):
        return self.__request__.get_text(url)

    def get_tree(self, url):
        html = self.get_html(url)
        return etree.HTML(html)

    def download_image(self, **kwargs):
        path = kwargs["path"]
        url = kwargs["url"]

        if path and url:
            content = self.__request__.get_content(url)

            if content:
                folder = os.path.dirname(path)

                if not os.path.exists(folder):
                    Path(folder).mkdir(exist_ok=True)

                with open(path, "ab") as file:
                    file.write(content)
                return True
            else:
                print(f'图片[{url}]下载出错')
                return False


