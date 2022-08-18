import os
import re

from modules.service.movie_warehouse.collate.film import Film


def find_configuration_node(json_setting, name):
    for website in json_setting:
        if website['name'] == name:
            return website['url']


class BaseMarauder(object):
    def __init__(self, **kwargs):
        self.__file__ = kwargs['file']
        self.__http_request__ = kwargs['request']

        self.__content__, self.__id__, self.__title__, self.__poster__, self.__stills__ = None, None, None, None, None

    def to_film(self) -> Film:
        if self.__content__ is None:
            raise Exception("没有获取到页面内容")

        return Film(self.__file__
                    , content=self.__content__
                    , id=self.__id__
                    , title=self.__format_title__()
                    , poster=self.__get_poster__()
                    , stills=self.__get_stills__())

    def __get_url_content__(self, url):
        response = self.__http_request__.get(url)

        if response:
            return response.text
        else:
            raise Exception('get url content error, response status code:' + str(response.status_code))

    def __format_title__(self):
        return re.compile("[?:*'<>./\\\]").sub("", self.__title__).strip()

    def __get_poster__(self):
        if self.__content__ is None:
            return None

        name = self.__id__ + os.path.splitext(self.__poster__)[-1]
        return {
            "name": name,
            "url": self.__poster__,
        }

    def __get_stills__(self):
        stills = []
        if self.__content__ is None:
            return None

        if self.__stills__ is not None and len(self.__stills__) > 0:
            for index in range(0, len(self.__stills__)):
                url = self.__stills__[index]
                name = os.path.split(url)[-1]
                type = name.split('.')[-1]

                stills.append({
                    "name": '%s_%s.%s' % (self.__id__, index, type),
                    "url": url,
                })

        return stills
