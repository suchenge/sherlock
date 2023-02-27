class MovieInformation(object):
    def __init__(self):
        self.__url__ = None
        self.__id__ = None
        self.__title__ = None
        self.__poster__ = None
        self.__stills__ = []
        self.__torrents__ = []

    @property
    def url(self) -> str:
        return self.__url__

    @url.setter
    def url(self, value: str):
        self.__url__ = value

    @property
    def id(self) -> str:
        return self.__id__

    @id.setter
    def id(self, value: str):
        self.__id__ = value

    @property
    def title(self) -> str:
        return self.__id__

    @title.setter
    def title(self, value: str):
        self.__title__ = value

    @property
    def poster(self):
        return self.__poster__

    @poster.setter
    def poster(self, value):
        self.__poster__ = value

    @property
    def stills(self) -> []:
        return self.__stills__

    @stills.setter
    def stills(self, value: []):
        self.__stills__ = value

    @property
    def torrents(self) -> []:
        return self.__torrents__

    @torrents.setter
    def torrents(self, value: []):
        self.__torrents__ = value

    def to_json(self):
        return {
            "url": self.__url__,
            "id": self.__id__,
            "title": self.__title__,
            "poster": self.__poster__,
            "stills": self.__stills__,
            "torrents": self.__torrents__
        }
