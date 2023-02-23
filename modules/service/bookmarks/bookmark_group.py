import os
import json

from threading import Lock
from pathlib import Path

from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool

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
        self.__lock__ = Lock()
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

    def __done__(self):
        if os.path.exists(self.__bak_file_path__):
            os.remove(self.__bak_file_path__)

        if os.path.exists(self.__file_path__):
            os.rename(self.__file_path__, self.__done_file_path__)

        if os.path.exists(self.__done_file_path__):
            self.save(self.__done_file_path__)

    def __bak__(self):
        if os.path.exists(self.__bak_file_path__):
            os.remove(self.__bak_file_path__)

        os.popen("copy %s %s" % (self.__file_path__, self.__bak_file_path__))
        # os.rename(self.__file_path__, self.__bak_file_path__)

        # self.save(self.__bak_file_path__)

    def save(self, file_path=None):
        if file_path is None:
            file_path = self.__file_path__

        folder = os.path.dirname(file_path)
        if not os.path.exists(folder):
            Path(folder).mkdir(exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([item.to_json() for item in self.items], file, indent=4, ensure_ascii=False)

    def __is_all_done__(self):
        is_done = True

        for item in self.items:
            if item.status != "done":
                is_done = False
                break

        return is_done

    def inspection(self):
        self.__lock__.acquire()

        if len(self.items) > 0:
            if self.__is_all_done__():
                self.__done__()
            else:
                self.__bak__()
                TaskPool.append_task(Task(self.inspection, None))

        self.__lock__.release()

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
        self.__bak__()

        inspection_count = 0
        process_count = 0

        for item in self.items:
            process_count = process_count + 1
            if item.status == "done":
                item.inspection(request)
                continue

            film = build_film_function(item.to_json())
            item.download(film, request)
            inspection_count = inspection_count + 1

            if inspection_count == 10 or process_count >= len(self.items):
                inspection_count = 0
                TaskPool.append_task(Task(self.inspection))

        TaskPool.join()


   