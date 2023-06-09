import os
import re

def __01__(content):
    match = re.search('链接[：|:](.*?) 密码[：|:](.*)', content).groups()
    return True, match[0], match[1]

def __02__(content):
    match = re.search('链接：(.*?) \n提取码：(.*)', content).groups()
    return True, match[0], match[1]

def __list__():
    return [__01__, __02__]

class LinkStatus(object):
    normal = "normal",
    resolve = "resolve"

class Link(object):
    def __init__(self, file_path):
        self.__file_path__ = file_path

        self.__url__ = None
        self.__password__ = None
        self.__status__ = LinkStatus.normal

    def __resolve__(self):
        with open(self.__file_path__, 'r') as file:
            content = file.read()

        success = False

        for r in __list__():
            try:
                success, self.__url__, self.__password__ = r(content)

                if success and self.__url__ and self.__password__:
                    break
            except Exception as error:
                pass

        if success is False:
            self.__status__ = LinkStatus.resolve

    def write(self, browser):
        try:
            self.__resolve__()

            if self.__status__ != LinkStatus.normal:
                raise
            #os.remove(self.__file_path__)
        except Exception as error:
            os.rename(self.__file_path__, f'{self.__file_path__}.{self.__status__}.error')
