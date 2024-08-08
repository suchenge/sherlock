class Label(object):
    def __init__(self):
        self.__url__ = None
        self.__title__ = None
        self.__uid__ = None
        self.__poster__ = None
        self.__stills__ = []

    @property
    def url(self) -> str:
        return self.__url__

    @url.setter
    def url(self, value: str):
        self.__url__ = value

    @property
    def uid(self) -> str:
        return self.__uid__

    @uid.setter
    def uid(self, value: str):
        self.__uid__ = value

    @property
    def title(self) -> str:
        return self.__title__

    @title.setter
    def title(self, value: str):
        self.__title__ = value

    @property
    def poster(self) -> str:
        return self.__poster__

    @poster.setter
    def poster(self, value: str):
        self.__poster__ = value

    @property
    def stills(self) -> list:
        return self.__stills__

    @stills.setter
    def stills(self, value: list):
        self.__stills__ = value
