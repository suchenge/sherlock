import os
import json

from pathlib import Path
from threading import Lock

from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool

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

        self.__lock__ = Lock()
        self.__inspection_count__ = 0

    def build(self, item):
        self.__href__ = item["href"]
        self.__title__ = item["title"]
        # self.__title__ = item["key"]
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
            result["resource"] = self.__information__

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

            self.inspection(request)
        except Exception as error:
            self.__status__ = "error"

    def inspection(self, request):
        self.__inspection__(request)

    def __inspection__(self, request):
        self.__lock__.acquire()

        path = self.__path__
        information_file_path = os.path.join(path, self.__information_file_name__)
        information = None
        done = True

        self.__inspection_count__ = self.__inspection_count__ + 1
        if self.__inspection_count__ >= 3:
            self.__done__(information_file_path)
            self.__lock__.release()
            return

        if self.__path__ and os.path.exists(path) and os.path.exists(information_file_path):
            with open(information_file_path, 'r', encoding='utf-8') as file:
                information = json.load(file)

        if information is not None:
            resource = information["resource"]
            file_infos = [{"name": still["name"], "url": still["url"]} for still in resource["stills"]]
            file_infos.append({"name": resource["poster"]["name"], "url": resource["poster"]["url"]})

            for file_info in file_infos:
                file_path = os.path.join(path, file_info["name"])
                if not os.path.exists(file_path):
                    done = False
                    Porter(None).save_file(file_info["url"], file_path, request)
        else:
            done = False

        if done is True:
            self.__done__(information_file_path)
            self.__lock__.release()
        else:
            self.__lock__.release()
            TaskPool.append_task(Task(self.__inspection__, request, 3))

    def __done__(self, file_path):
        self.__status__ = "done"

        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            Path(folder).mkdir(exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.to_json(True), file, indent=4, ensure_ascii=False)

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
