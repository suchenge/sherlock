import os

from pathlib import Path

from modules.tools.http_request.request import Request
from modules.tools.http_request.proxy import Proxies


class HttpClient(object):
    __proxies__ = None
    __request__ = Request(__proxies__)

    @staticmethod
    def set_proxies(proxies: Proxies):
        HttpClient.__proxies__ = proxies
        HttpClient.__request__ = Request(proxies)

    @staticmethod
    def get_text(url: str):
        return HttpClient.__request__.get_text(url)

    @staticmethod
    def get_content(url: str):
        return HttpClient.__request__.get_content(url)

    @staticmethod
    def download(**kwargs):
        path = kwargs["path"]
        url = kwargs["url"]

        if path and url:
            folder = os.path.dirname(path)

            if not os.path.exists(folder):
                Path(folder).mkdir(exist_ok=True)

            content = HttpClient.get_content(url)

            if content:
                with open(path, "ab") as file:
                    file.write(content)
