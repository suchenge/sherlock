import os


class VideoPath(object):
    def __init__(self, path):
        self.__path__ = path

        self.__analysis__()

    def __analysis__(self):
        self.__parent__, self.__name__ = os.path.split(self.__path__)

        if os.path.isfile(self.__path__):
            self.__type__ = self.__name__.split('.')[-1]
            self.__uid__ = self.__name__.replace(self.__type__, '').strip('.').split(' ')[0]
            self.__title__ = self.__name__.replace(self.__uid__, '').replace(self.__type__, '').strip('.')
        else:
            dismantle_name = self.__name__.split(' ')
            self.__uid__ = dismantle_name[0]
            self.__title__ = self.__name__.replace(self.__uid__, '').strip()

    @property
    def uid(self) -> str:
        return self.__uid__.upper()

    @property
    def path(self) -> str:
        return self.__path__

    @property
    def parent(self) -> str:
        return self.__parent__

    @property
    def name(self) -> str:
        return self.__name__

    @property
    def title(self) -> str:
        return self.__title__

    @property
    def type(self) -> str:
        return self.__type__


