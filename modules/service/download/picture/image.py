from modules.tools.common_methods.unity_tools import get_file_suffix

class Image(object):
    def __init__(self, url):
        self.__url__ = url
        self.__file_name__ = None
        self.__main_url__ = None
        self.__main_title__ = None
        self.__sub_url__ = None
        self.__sub_title__ = None
        self.__suffix__ = get_file_suffix(url)

    @property
    def url(self):
        return self.__url__

    @property
    def file_name(self):
        return self.__file_name__

    @file_name.setter
    def file_name(self, name):
        self.__file_name__ = name

    @property
    def main_url(self):
        return self.__main_url__

    @main_url.setter
    def main_url(self, main_url):
        self.__main_url__ = main_url

    @property
    def main_title(self):
        return self.__main_title__

    @main_title.setter
    def main_title(self, main_title):
        self.__main_title__ = main_title

    @property
    def sub_url(self):
        return self.__sub_url__

    @sub_url.setter
    def sub_url(self, sub_url):
        self.__sub_url__ = sub_url

    @property
    def sub_title(self):
        return self.__sub_title__

    @sub_title.setter
    def sub_title(self, sub_title):
        self.__sub_title__ = sub_title

    @property
    def suffix(self):
        return self.__suffix__

    @staticmethod
    def build(info: dict):
        result = Image(info['url'])

        result.file_name = info['file_name']
        result.main_url = info['main_url']
        result.main_title = info['main_title']
        result.sub_url = info['sub_url']
        result.sub_title = info['sub_title']

        return result

    def to_dict(self):
        return {
                'url': self.url,
                'file_name': self.file_name,
                'main_url': self.main_url,
                'main_title': self.main_title,
                'sub_url': self.sub_url,
                'sub_title': self.sub_title
            }
