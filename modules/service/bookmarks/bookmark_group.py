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

    @staticmethod
    def build(file_path):
        if os.path.isfile(file_path) and "bookmark_group" in file_path:
            folder = os.path.dirname(file_path)
            index = re.compile(r'bookmark_group_(\d+)\.json').findall(file_path)[0]

            return BookmarkGroup(os.path.dirname(file_path), index)
        return None

    def inspection(self):
        if len(self.__items__) > 0:
            items = [item.to_json() for item in self.__items__]

            if not os.path.exists(self.__file_path__):
                with open(self.__file_path__, 'w', encoding='utf-8') as file:
                    json.dump(items, file, indent=4, ensure_ascii=False)

            else:
                bak_file_path = self.__file_path__ + ".bak"

                if os.path.exists(bak_file_path):
                    os.remove(bak_file_path)

                os.rename(self.__file_path__, bak_file_path)

                with open(self.__file_path__, 'w', encoding='utf-8') as file:
                    json.dump(items, file, indent=4, ensure_ascii=False)

    @property
    def items(self):
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
            inspection_count = inspection_count + 1
            process_count = process_count + 1

            film = build_film_function(item.to_json())
            item.download(film, request)

            if inspection_count == 10 or process_count >= item_length:
                inspection_count = 0
                TaskPool.append_task(Task(self.inspection))


