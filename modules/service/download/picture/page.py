class Page(object):
    def __init__(self):
        self.__url__ = None
        self.__html__ = None
        self.__title__ = None
        self.__index__ = 0

    @property
    def url(self):
        return self.__url__

    @url.setter
    def url(self, url):
        self.__url__ = url

    @property
    def html(self):
        return self.__html__

    @html.setter
    def html(self, html):
        self.__html__ = html

    @property
    def title(self):
        return self.__title__

    @title.setter
    def title(self, title):
        self.__title__ = title

    @property
    def index(self):
        return self.__index__

    @index.setter
    def index(self, index):
        self.__index__ = index

    @staticmethod
    def build(info: dict):
        result = Page()

        result.url = info['url']
        result.index = info['index']

        return result
