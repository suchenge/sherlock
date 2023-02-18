import os
import json

from modules.service.movie_warehouse.collate.film import Film
from modules.service.movie_warehouse.collate.porter import Porter


class Bookmark(object):
    def __init__(self):
        self.__href__ = None
        self.__title__ = None
        self.__key__ = None
        self.__index__ = None
        self.__status__ = None
        self.__path__ = None
        self.__information__ = None

        self.__information_file_name__ = "information.json"

    def build(self, item):
        self.__href__ = item["href"]
        self.__title__ = item["title"]
        self.__key__ = item["key"]
        self.__index__ = item["index"]
        self.__status__ = item["status"]

        if item.get("path"):
            self.__path__ = item.get("path")
            information_file_path = os.path.join(self.__path__, self.__information_file_name__)

            if os.path.exists(information_file_path):
                with open(information_file_path, 'r', encoding='utf-8') as file:
                    self.__information__ = json.load(file)

        return self

    def to_json(self, save_information=False):
        result = {
            "href": self.__href__,
            "title": self.__title__,
            "key": self.__key__,
            "index": self.__index__,
            "status": self.__status__
        }

        if self.__path__:
            result["path"] = self.__path__

        if self.__information__ and save_information:
            result["information"] = self.__information__

        return result

    def download(self, film: Film, request):
        self.__path__ = film.folder
        self.__status__ = 'downloading'
        self.__information__ = {
            "id": film.id,
            "title": film.title,
            "url": film.url,
            "poster": {"name": film.poster["name"], "url": film.poster["url"]},
            "stills": [{"name": still["name"], "url": still["url"]} for still in film.stills],
            "torrents": [{"name": torrent["name"], "url": torrent["url"], "link": torrent["link"]} for torrent in film.torrents]
        }

        try:
            porter = Porter(film)
            porter.save_information(self.to_json(True), self.__information_file_name__)
            porter.save_poster(request)
            porter.save_stills(request)
        except Exception as error:
            self.__status__ = "error"

    def inspection(self, request):
        path = self.__path__
        information_file_path = os.path.join(path, self.__information_file_name__)
        information = None
        result = True

        if self.__path__ and os.path.exists(path) and os.path.exists(information_file_path):
            with open(information_file_path, 'r', encoding='utf-8') as file:
                information = json.load(file)
        else:
            self.__status__ = "open"
            result = False

        if information:
            file_infos = [{"name": still["name"], "url": still["url"]} for still in information["stills"]]
            file_infos.append({"name": information["poster"]["name"], "url": information["poster"]["url"]})

            for file_info in file_infos:
                if not os.path.exists(file_info["path"]):
                    Porter(None).save_file(file_info["url"], os.path.join(path, file_info["path"]), request)
                    result = False

        return result

    @property
    def href(self):
        return self.__href__

    @href.setter
    def href(self, value):
        self.__href__ = value

    @property
    def title(self):
        return self.__href__

    @title.setter
    def title(self, value):
        self.__title__ = value

    @property
    def key(self):
        return self.__key__

    @key.setter
    def key(self, value):
        self.__key__ = value

    @property
    def index(self):
        return self.__index__

    @index.setter
    def index(self, value):
        self.__index__ = value

    @property
    def status(self):
        return self.__status__

    @status.setter
    def status(self, value):
        self.__status__ = value

    @property
    def path(self):
        return self.__path__

    @property
    def information(self):
        return self.__information__
