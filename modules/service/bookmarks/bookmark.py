import os
import json
import shutil

from pathlib import Path

from modules.tools.http_request.http_client import HttpClient

from modules.service.movie_marauder.movie_information import MovieInformation
from modules.service.movie_marauder.javdb_marauder import JavdbMarauder


class Bookmark(object):
    def __init__(self, **kwargs):
        self.__href__ = kwargs["href"]
        self.__title__ = kwargs["title"]
        self.__key__ = kwargs["key"]
        self.__index__ = kwargs["index"]
        self.__status__ = kwargs["status"]

        self.__path__ = None
        if kwargs.get("path"):
            self.__path__ = kwargs["path"]

        self.__information_file_name__ = "information.json"
        self.__information__ = None

    @property
    def path(self):
        return self.__path__

    @property
    def status(self) -> str:
        return self.__status__

    @status.setter
    def status(self, value):
        self.__status__ = value

    def get_information(self, information_folder) -> MovieInformation:
        information_path = os.path.join(information_folder, self.__information_file_name__)

        if os.path.exists(information_path):
            print("获取存在的information信息|" + information_path)

            with open(information_path, "r", encoding="utf-8") as file:
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
        return None

    def to_json(self, information=None, save_path=None):
        result = {
            "href": self.__href__,
            "title": self.__title__,
            "key": self.__key__,
            "index": self.__index__,
            # "status": self.__status__
        }

        if save_path:
            self.__path__ = result["path"] = save_path

        if information:
            result["resource"] = information.to_json()

        if self.__path__:
            result["path"] = self.__path__

        return result

    def download(self, save_folder):
        save_path = None

        try:
            javdb_url = self.__href__
            movie_info = None

            marauder = JavdbMarauder()

            if not marauder.is_match(self.__href__):
                javdb_url = marauder.search(self.__key__)

            if javdb_url:
                movie_info = marauder.get_movie(javdb_url)

            if movie_info:
                save_path = os.path.join(save_folder, movie_info.title)

                if not os.path.exists(save_path):
                    Path(save_path).mkdir(exist_ok=True)

                information_path = os.path.join(save_path, self.__information_file_name__)

                with open(information_path, "w", encoding="utf-8") as file:
                    json.dump(self.to_json(movie_info, save_path), file, indent=4, ensure_ascii=False)

                    if movie_info.poster:
                        HttpClient.download(**{"path": os.path.join(save_path, movie_info.poster["name"]), "url": movie_info.poster["url"]})

                    if movie_info.stills and len(movie_info.stills) > 0:
                        for still in movie_info.stills:
                            HttpClient.download(**{"path": os.path.join(save_path, still["name"]), "url": still["url"]})
                self.__status__ = "done"
        except Exception as error:
            self.delete(save_path)
            raise error

    def inspection(self, information):
        try:
            items = [{"path": os.path.join(self.__path__, still["name"]), "url": still["url"]} for still in information.stills]
            items.append({"path": os.path.join(self.__path__, information.poster["name"]), "url": information.poster["url"]})

            if items and len(items) > 0:
                for item in items:
                    if not os.path.exists(item["path"]):
                        HttpClient.download(**{"path": item["path"], "url": item["url"]})
        except Exception as error:
            self.delete(self.__path__)
            raise error

    def delete(self, save_path):
        self.__status__ = "error"

        if os.path.exists(save_path):
            shutil.rmtree(save_path)


            




