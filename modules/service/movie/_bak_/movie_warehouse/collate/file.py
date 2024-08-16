import os
import re


def __rename_filename__(source, target):
    if os.path.exists(target):
        os.remove(target)
    else:
        os.rename(source, target)


class File(object):
    def __init__(self, path):
        if '.exception' in path:
            new_path = path.replace('.exception', '')
            __rename_filename__(path, new_path)
            path = new_path

        redundants = ['-A.torrent', '-fuckbe.torrent', '.VR.torrent', '_4K-A.torrent', ' 【VR】.torrent',
                      '  [VR].torrent', '_VR.torrent', '_4K.torrent']

        for redundant in redundants:
            if redundant in path:
                new_path = path.replace(redundant, '.torrent')
                __rename_filename__(path, new_path)
                path = new_path

        search = re.search(r'\d( .*?)\.torrent', path)
        if search is not None:
            new_path = path.replace(search.group(1), '')
            __rename_filename__(path, new_path)
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
        return 'name：%s\n type：%s\n title：%s\n folder：%s\n path：%s\n' % (
            self.name, self.type, self.title, self.folder, self.path)

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


class VirtualFile(File):
    def __init__(self, obj):
        self.__folder__ = obj["folder"]
        self.__name__ = obj["name"]
        self.__title__ = obj["title"]
        self.__path__ = obj["path"]
        self.__url__ = obj["url"]

    @property
    def url(self):
        return self.__url__

    @property
    def need_search(self):
        return 'javdb.com/v/' not in self.__url__


