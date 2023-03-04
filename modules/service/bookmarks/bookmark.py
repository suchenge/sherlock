import os
import json

from pathlib import Path

from modules.tools.http_request.http_client import HttpClient
from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool

from modules.service.movie_marauder.movie_information import MovieInformation
from modules.service.movie_marauder.javdb_marauder import JavdbMarauder


class Bookmark(object):
    def __init__(self, **kwargs):
        self.__information__ = None

        self.__href__ = kwargs["href"]
        self.__title__ = kwargs["title"]
        self.__key__ = kwargs["key"]
        self.__index__ = kwargs["index"]
        self.__status__ = kwargs["status"]
        self.__group_path__ = kwargs["group_path"]

        self.__path__ = None
        self.__information_file_name__ = "information.json"
        self.__information_file_path__ = None
        self.__information__ = None

        if kwargs.get("path"):
            self.__path__ = kwargs["path"]
            self.__information_file_path__ = os.path.join(self.__path__, self.__information_file_name__)
            self.__information__ = self.__get_information_by_file__()

        self.__inspection_delay_seconds__ = 0
        self.__inspection_count__ = 0

        self.__group__ = None

    @property
    def group(self):
        return self.__group__

    @group.setter
    def group(self, value):
        self.__group__ = value

    @property
    def status(self) -> str:
        return self.__status__

    def __get_information_by_file__(self) -> MovieInformation:
        if self.__information__ is None:
            if os.path.exists(self.__information_file_path__):
                print("获取存在的information信息|" + self.__information_file_path__)

                with open(self.__information_file_path__, "r", encoding="utf-8") as file:
                    content_info = json.load(file)
                    if content_info and content_info.get("resource"):
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
            result["resource"] = self.__information__.to_json()

        return result

    def download(self):
        if self.__information__:
            self.__inspection__()
        else:
            javdb_url = self.__href__
            movie_info = None

            marauder = JavdbMarauder()

            if not marauder.is_match(self.__href__):
                javdb_url = marauder.search(self.__key__)

            if javdb_url:
                movie_info = marauder.get_movie(javdb_url)

            if movie_info:
                try:
                    self.__information__ = movie_info
                    self.__path__ = os.path.join(self.__group_path__, movie_info.title)
                    self.__save_information__()
                    self.__save_stills__()
                    self.__save_poster__()

                    # self.__inspection__()
                    TaskPool.append_task(Task(self.__inspection__, args=None, in_queue_delay_seconds=self.__max_inspection_count__()))
                except Exception as error:
                    self.__save__("error")
            else:
                self.__save__("error")

    def __save_information__(self):
        if not os.path.exists(self.__path__):
            Path(self.__path__).mkdir(exist_ok=True)

        if not self.__information_file_path__:
            self.__information_file_path__ = os.path.join(self.__path__, self.__information_file_name__)

        with open(self.__information_file_path__, "w", encoding="utf-8") as file:
            json.dump(self.to_json(True), file, indent=4, ensure_ascii=False)

    def __save_stills__(self):
        if self.__information__ and self.__information__.stills and len(self.__information__.stills):
            self.__append_download_tasks__(self.__information__.stills)

    def __save_poster__(self):
        if self.__information__ and self.__information__.poster:
            self.__append_download_task__(os.path.join(self.__path__, self.__information__.poster["name"]), self.__information__.poster["url"])

    def __append_download_task__(self, name, url):
        if name and url:
            file_path = os.path.join(self.__path__, name)

            if not os.path.exists(file_path):
                self.__inspection_delay_seconds__ = self.__inspection_delay_seconds__ + 1
                task = Task(HttpClient.download, kwargs={"path": os.path.join(self.__path__, name), "url": url})
                TaskPool.append_task(task)

    def __append_download_tasks__(self, items):
        for item in items:
            self.__append_download_task__(item["name"], item["url"])

    def __max_inspection_count__(self):
        if self.__information__ and self.__information__.stills and len(self.__information__.stills):
            self.__inspection_delay_seconds__ = len(self.__information__.stills)
        return self.__inspection_delay_seconds__
        '''
        if self.__information__ and self.__information__.stills and len(self.__information__.stills) > 0:
            return len(self.__information__.stills) * 2
        else:
            return 10
        '''

    def __group_inspection__(self):
        if self.__group__:
            self.__group__.inspection()

    def __inspection__(self):
        if self.__inspection_count__ >= self.__max_inspection_count__():
            self.__save__("error")
            self.__group_inspection__()
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
                self.__save__("done")
                self.__group_inspection__()
            else:
                TaskPool.append_task(Task(self.__inspection__, args=None, in_queue_delay_seconds=5))

    def __save__(self, status="done"):
        self.__status__ = status

        folder = os.path.dirname(self.__information_file_path__)
        if not os.path.exists(folder):
            Path(folder).mkdir(exist_ok=True)

        with open(self.__information_file_path__, 'w', encoding='utf-8') as file:
            json.dump(self.to_json(True), file, indent=4, ensure_ascii=False)


