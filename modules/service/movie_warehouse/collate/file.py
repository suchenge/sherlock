import os


class File(object):
    def __init__(self, path):
        if '.exception' in path:
            new_path = path.replace('.exception', '')
            os.rename(path, new_path)
            path = new_path
            
        self.__path__ = path

        if os.path.isfile(path):
            self.__folder__, self.__name__ = os.path.split(path)
            self.__type__ = self.__name__.split('.')[-1]
            self.__title__ = self.__name__.replace(self.__type__, '').strip('.')
        else:
            self.__folder__ = os.path.dirname(path)
            self.__title__ = self.__name__ = path.replace(self.__folder__, '')

    def __str__(self):
        return 'name：%s\n type：%s\n title：%s\n folder：%s\n path：%s\n' % (self.name, self.type, self.title, self.folder, self.path)

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
