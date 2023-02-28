import os
import json

from pathlib import Path

from modules.tools.http_request.request import Request, download
from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool

from modules.service.movie_marauder.movie_information import MovieInformation
from modules.service.movie_marauder.javdb_marauder import JavdbMarauder


class Bookmark(object):
    def __init__(self, json_info: {}):
        self.__href__ = json_info["href"]
        self.__title__ = json_info["title"]
        self.__key__ = json_info["key"]
        self.__index__ = json_info["index"]
        self.__status__ = json_info["status"]
        self.__path__ = json_info["path"]

        self.__information_file_name__ = "information.json"
        self.__information_file_path__ = os.path.join(self.__path__, self.__information_file_name__)

        self.__information__ = self.__get_information_by_file__()
        self.__request__ = None
        self.__inspection_count__ = 0

    @property
    def status(self) -> str:
        return self.__status__

    def __get_information_by_file__(self) -> MovieInformation:
        if self.__information__ is None:
            if os.path.exists(self.__information_file_path__):
                with open(self.__information_file_path__, "r", encoding="utf-8") as file:
                    content_info = json.load(file)
                    info = content_info["resource"]

                    self.__information__ = MovieInformation()
                    self.__information__.id = info["id"]
                    self.__information__.title = info["title"]
                    self.__information__.url = info["url"]
                    self.__information__.poster = info["poster"]
                    self.__information__.stills = info["stills"]
                    self.__information__.torrents = info["torrents"]

        return self.__information__

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

    def download(self, request: Request):
        self.__request__ = request

        if self.__information__:
            self.__inspection__()
        else:
            movie_info = JavdbMarauder(self.__href__, request).get_movie()

            if movie_info:
                self.__information__ = movie_info
                self.__save_information__()
                self.__save_stills__()
                self.__save_poster__()

                self.__inspection__()
            else:
                self.__save__("error")

    def __save_information__(self):
        if not os.path.exists(self.__path__):
            Path(self.__path__).mkdir(exist_ok=True)

        with open(self.__information_file_path__, "w", encoding="utf-8") as file:
            json.dump(self.to_json(True), file, indent=4, ensure_ascii=False)

    def __save_stills__(self):
        if self.__information__ and self.__information__.stills and len(self.__information__.stills):
            self.__append_download_tasks__(self.__information__.stills)

    def __save_poster__(self):
        if self.__information__ and self.__information__.poster:
            self.__append_download_task__(self.__information__.poster["path"], self.__information__.poster["url"])

    def __append_download_task__(self, path, url):
        if path and url:
            task = Task(download, kwargs={"request": self.__request__, "path": path, "url": url})
            TaskPool.append_task(task)

    def __append_download_tasks__(self, items):
        for item in items:
            self.__append_download_task__(item["path"], item["url"])

    def __build_download_task__(self, path, url):
        if path and url:
            return Task(download, kwargs={"request": self.__request__, "path": path, "url": url})

    def __max_inspection_count__(self):
        if self.__information__ and self.__information__.stills and len(self.__information__.stills) > 0:
            return len(self.__information__.stills) * 2
        else:
            return 10

    def __inspection__(self):
        if self.__inspection_count__ >= self.__max_inspection_count__():
            self.__save__("error")
        else:
            self.__inspection_count__ = self.__inspection_count__ + 1

            items = [{"path": os.path.join(self.__path__, still["name"]), "url": still["url"]} for still in self.__information__.stills]
            items.append({"path": os.path.join(self.__path__, self.__information__.poster["name"]), "url": self.__information__.poster["url"]})

            done = True
            if items and len(items) > 0:
                for item in items:
                    if not os.path.exists(item["path"]):
                        done = False
                        self.__append_download_task__(item["path"], item["url"])

            if done:
                self.__save__()
            else:
                TaskPool.append_task(Task(self.__inspection__, args=None, in_queue_delay_seconds=5))

    def __save__(self, status="done"):
        self.__status__ = status

        folder = os.path.dirname(self.__information_file_path__)
        if not os.path.exists(folder):
            Path(folder).mkdir(exist_ok=True)

        with open(self.__information_file_path__, 'w', encoding='utf-8') as file:
            json.dump(self.to_json(True), file, indent=4, ensure_ascii=False)


