from modules.tools.http_request.proxy import Proxies
from modules.tools.http_request.request import Request

from modules.service.movie.analysis.analyzer_base import AnalyzerBase
from modules.service.movie.analysis.analyzer_javdb import AnalyzerJavdb
from modules.service.movie.analysis.information import Information


class Analyst:
    def __init__(self, uid: str):
        self.__uid__ = uid
        self.__request__ = None

    def __get_information__(self, analyzer: AnalyzerBase) -> Information | None:
        try:
            result = analyzer.get_information(self.__uid__)
        except Exception as e:
            result = None

        return result

    @property
    def request(self) -> Request | None:
        return self.__request__

    def get_information(self) -> Information:
        proxy_request = Request(Proxies())

        analyzer_creator = [
            lambda x: AnalyzerJavdb(proxy_request),
        ]

        result = None

        for item in analyzer_creator:
            analyzer = item(None)
            result = self.__get_information__(analyzer)

            if result is not None:
                self.__request__ = analyzer.request
                return result

        if result is None:
            raise Exception("没有获取到解析的信息")
