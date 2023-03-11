import os
import json

from pathlib import Path

from modules.service.bookmarks.bookmark import Bookmark


class BookmarkGroups(object):
    def __init__(self, folder):
        self.__folder__ = folder
        self.__groups_file_index__ = []
        self.__index_file_path__ = os.path.join(folder, "bookmarks.json")

        if os.path.exists(self.__index_file_path__):
            with open(self.__index_file_path__, 'r', encoding='utf-8') as file:
                self.__groups_path__ = json.load(file)

    def append_group_path(self, bookmark_group_path):
        if bookmark_group_path not in self.__groups_file_index__:
            self.__groups_file_index__.append(bookmark_group_path)

    def save(self):
        if len(self.__groups_file_index__) > 0:
            with open(self.__index_file_path__, "w", encoding="utf-8") as file:
                json.dump(self.__groups_file_index__, file, indent=4, ensure_ascii=False)

    def get_items(self):
        result = []

        if len(self.__groups_path__) > 0:
            for group_path in self.__groups_path__:
                if os.path.exists(group_path):
                    result.append(BookmarkGroup(os.path.dirname(group_path)))

        return result


class BookmarkGroup(object):
    def __init__(self, folder):
        self.__items__ = []
        self.__base_name__ = "bookmarks.json"
        self.__file_path__ = os.path.join(folder, self.__base_name__)

        self.__bak_file_path__ = self.__file_path__ + ".bak"
        self.__done_file_path__ = self.__file_path__.replace("json", "done.json")

    @property
    def file_path(self):
        return self.__file_path__

    @property
    def folder(self):
        return os.path.dirname(self.__file_path__)

    @property
    def items(self):
        if len(self.__items__) == 0:
            with open(self.__file_path__, 'r', encoding='utf-8') as file:
                for item in json.load(file):
                    item["group_path"] = self.folder
                    bookmark = Bookmark(**item)
                    bookmark.group = self
                    self.__items__.append(bookmark)

        return self.__items__

    @items.setter
    def items(self, value):
        self.__items__ = value

    def download(self):
        for item in self.items:
            item.download()

    def save(self):
        self.__bak__()
        self.__save_items__()

    def __create_folder__(self, file_path):
        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            Path(folder).mkdir(exist_ok=True)

    def __bak__(self):
        if not os.path.exists(self.__file_path__):
            return

        if os.path.exists(self.__bak_file_path__):
            os.remove(self.__bak_file_path__)

        os.popen("copy %s %s" % (self.__file_path__, self.__bak_file_path__))

    def __save_items__(self):
        done_items = list(filter(lambda item: item.status == "done", self.items))
        self.__save_items_for_file__(done_items, self.__done_file_path__)

        if len(self.items) == len(done_items):
            os.remove(self.__file_path__)

            if os.path.exists(self.__bak_file_path__):
                os.remove(self.__bak_file_path__)

    def __save_items_for_file__(self, items, file_path):
        if items is None or len(items) <= 0:
            return

        self.__create_folder__(file_path)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([item.to_json() for item in items], file, indent=4, ensure_ascii=False)


   