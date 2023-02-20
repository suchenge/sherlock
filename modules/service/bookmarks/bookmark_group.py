import os
import re
import json

from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool

from modules.service.bookmarks.bookmark import Bookmark


class BookmarkGroup(object):
    def __init__(self, folder, index):
        self.__items__ = []
        self.__base_name__ = "bookmark_group_%s.json" % index
        self.__file_path__ = os.path.join(folder, self.__base_name__)

        self.__bak_file_path__ = self.__file_path__ + ".bak"
        self.__done_file_path__ = self.__file_path__.replace("json", "done.json")

    @staticmethod
    def build(file_path):
        if os.path.isfile(file_path) and "bookmark_group" in file_path and "done" not in file_path:
            index = re.compile(r'bookmark_group_(\d+)\.json').findall(file_path)[0]

            return BookmarkGroup(os.path.dirname(file_path), index)
        return None

    def __done__(self):
        if os.path.exists(self.__bak_file_path__):
            os.remove(self.__bak_file_path__)

        os.rename(self.__file_path__, self.__done_file_path__)
        self.__save__(self.__done_file_path__)

    def __bak__(self):
        if os.path.exists(self.__bak_file_path__):
            os.remove(self.__bak_file_path__)
            os.rename(self.__file_path__, self.__bak_file_path__)

        self.__save__(self.__file_path__)

    def __save__(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([item.to_json() for item in self.__items__], file, indent=4, ensure_ascii=False)

    def __is_all_done__(self):
        return len([item for item in self.items if item.status == "done"]) == len(self.items)

    def inspection(self):
        if len(self.items) > 0:
            if self.__is_all_done__():
                self.__done__()
            else:
                self.__bak__()
                TaskPool.append_task(Task(self.inspection, None))

    @property
    def items(self):
        if len(self.__items__) == 0:
            with open(self.__file_path__, 'r', encoding='utf-8') as file:
                self.__items__ = [Bookmark().build(item) for item in json.load(file)]

        return self.__items__

    @items.setter
    def items(self, value):
        self.__items__ = value

    def download(self, build_film_function, request):
        inspection_count = 0
        process_count = 0
        item_length = len(self.items)

        for item in self.items:
            process_count = process_count + 1
            if item.status == "done":
                item.inspection(request)
                continue

            film = build_film_function(item.to_json())
            item.download(film, request)
            inspection_count = inspection_count + 1

            if inspection_count == 10 or process_count >= item_length:
                inspection_count = 0
                TaskPool.append_task(Task(self.inspection))

        TaskPool.join()


