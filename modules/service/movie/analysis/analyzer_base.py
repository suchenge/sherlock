from modules.tools.http_request.request import Request

from modules.service.movie.analysis.information import Information


class AnalyzerBase(object):
    def __init__(self, request: Request):
        self.__request__ = request

    def get_information(self, uid: str) -> Information:
        pass

    @property
    def request(self):
        return self.__request__

    def __get_url_content__(self, url):
        response = self.__request__.get_content(url)

        if response:
            return response
        else:
            raise Exception("没有获取到页面内容:" + url)
