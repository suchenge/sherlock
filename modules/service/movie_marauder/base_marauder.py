from lxml import etree

from modules.tools.http_request.request import Request

from modules.service.movie_marauder.movie_information import MovieInformation


class BaseMarauder(object):
    def __init__(self, url: str, request: Request):
        self.__url__ = url
        self.__request__ = request

        self.__html_content__ = None
        self.__html_tree__ = None

    def get_movie(self) -> MovieInformation:
        result = None
        try:
            self.__html_content__ = self.__request__.get_text(self.__url__)
            if self.__html_content__:
                self.__html_tree__ = etree.HTML(self.__html_content__)
                if self.__html_tree__:
                    result = MovieInformation()
                    result.url = self.__url__
                    result.id = self.__get_id__()
                    result.poster = self.__get__poster__()
                    result.title = self.__get_title__()
                    result.stills = self.__get_stills__()
                    result.torrents = self.__get_torrents__()

                    return result
        except Exception as error:
            pass

        return result

    def __get_id__(self) -> str:
        pass

    def __get_title__(self) -> str:
        pass

    def __get__poster__(self) -> {}:
        pass

    def __get_stills__(self) -> [{}]:
        pass

    def __get_torrents__(self) -> [{}]:
        pass




