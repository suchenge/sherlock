import os


class Film(object):
    def __init__(self, file, **kwargs):
        self.__file__ = file
        self.__content__, self.__id__, self.__title__, self.__poster__, self.__stills__, self.__torrents__ = kwargs['content'], kwargs['id'], kwargs['title'], kwargs['poster'], kwargs['stills'], kwargs['torrents']

    def __str__(self):
        return 'id:%s\n title:%s\n posters:%s\n stills:\n%s\n' % (self.id, self.title, self.poster['url'], '\n'.join(['       ' + stills['url'] for stills in self.stills]))

    @property
    def file(self):
        return self.__file__

    @property
    def id(self):
        return self.__id__

    @property
    def title(self):
        return self.__title__

    @property
    def content(self):
        return self.__content__

    @property
    def poster(self):
        self.__poster__['path'] = os.path.join(self.folder, self.__poster__['name'])
        return self.__poster__

    @property
    def stills(self):
        return [{'name': still['name'], 'url': still['url'], 'path': os.path.join(self.folder, still['name'])} for still in self.__stills__]

    @property
    def torrents(self):
        return [{'name': torrent['name'], 'url': torrent['url'], 'path': os.path.join(self.folder, torrent['name'])} for torrent in self.__torrents__] 

    @property
    def folder(self):
        if self.__title__ in self.__file__.folder:
            return self.__file__.folder
        return os.path.join(self.__file__.folder, self.__title__)
