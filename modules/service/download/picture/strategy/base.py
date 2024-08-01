import os

from pathlib import Path

from modules.tools.common_methods.unity_tools import parse_url
from modules.tools.http_request.request import Request

class Base(object):
    def __init__(self, url, html):
        self.__url__ = url
        self.__html__ = html
        self.__domain_url__, self.__url_path__ = parse_url(url)
        self.__request__ = Request()

    @staticmethod
    def is_match(url, html):
        return False

    def get_title(self):
        return None

    def get_child_page_url(self):
        return []

    def get_images(self, html, page_index=None):
        return []

    def get_html(self, url=None):
        if url is None:
            return self.__request__.get_text(self.__url__)
        else:
            return self.__request__.get_text(url)

    def download_image(self, **kwargs):
        path = kwargs["path"]
        url = kwargs["url"]

        if path and url:
            folder = os.path.dirname(path)

            if not os.path.exists(folder):
                Path(folder).mkdir(exist_ok=True)

            content = self.__request__.get_content(url)

            if content:
                with open(path, "ab") as file:
                    file.write(content)

