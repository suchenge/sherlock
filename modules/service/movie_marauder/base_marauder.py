import re

from lxml import etree

from modules.tools.http_request.http_client import HttpClient
from modules.service.movie_marauder.movie_information import MovieInformation


def find_configuration_node(json_setting, name):
    for website in json_setting:
        if website['name'] == name:
            return website['url']


def build_torrent_url(magent_url):
    match = re.compile(r'magnet\:\?xt=urn\:btih\:(.*?)&dn=.*?').findall(magent_url)
    if match:
        return 'https://itorrents.org/torrent/%s.torrent' % match[0]
    else:
        return None


class BaseMarauder(object):
    def __init__(self):
        self.__url__ = None
        self.__html_content__ = None
        self.__html_tree__ = None

    def get_movie(self, url: str) -> MovieInformation:
        self.__url__ = url
        result = None

        try:
            self.__html_content__ = HttpClient.get_text(self.__url__)
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
        finally:
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




