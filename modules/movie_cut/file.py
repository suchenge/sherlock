import os


class File(object):
    def __init__(self, path):
        self.__path__ = path
        self.__folder__, self.__name__ = os.path.split(path)
        self.__type__ = self.__name__.split('.')[-1]
        self.__title__ = self.__name__.replace(self.__type__, '').strip('.')

    @property
    def name(self):
        return self.__name__

    @property
    def title(self):
        return self.__title__

    @property
    def folder(self):
        return self.__folder__

    @property
    def path(self):
        return self.__path__

    @property
    def type(self):
        return self.__type__
