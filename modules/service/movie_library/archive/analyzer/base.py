from modules.tools.http_request.request import Request

from modules.service.movie_library.archive.label import Label

class Analyzer(object):
    def __init__(self, request: Request):
        self.__request__ = request

    def create_label(self, id: str) -> Label:
        pass

    def __get_url_content__(self, url):
        response = self.__request__.get_content(url)

        if response:
            return response
        else:
            raise Exception("没有获取到页面内容:" + url)
