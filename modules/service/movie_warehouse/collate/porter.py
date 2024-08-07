import json
import os
import shutil

from pathlib import Path

from modules.service.movie_warehouse.collate.film import Film
from modules.service.movie_warehouse.collate import dictionary
from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool


def __save_image__(args):
    image = args[0]
    request = args[1]

    path = image['path']
    url = image['url']

    if path is not None and url is not None:
        folder = os.path.dirname(path)

        if not os.path.exists(folder):
            Path(folder).mkdir(exist_ok=True)

        if 'torrent' in url:
            response = request.download(url)
        else:
            response = request.get(url)

        content = response.content

        with open(path, "ab") as fs:
            fs.write(content)


class Porter(object):
    def __init__(self, film: Film):
        self.__film__ = film

    @staticmethod
    def save_file(url, path, request):
        TaskPool.append_task(Task(__save_image__, [{"path": path, "url": url}, request]))

    def move(self):
        print("移动文件")
        film = self.__film__

        if not film.file.type:
            # 如果是文件夹，重命名文件夹
            os.rename(film.file.path, film.folder)
        else:
            # 如果是文件
            if not os.path.exists(film.folder):
                # 创建文件夹
                Path(film.folder).mkdir(exist_ok=True)

            # 判断需要移动的文件是否已经存在
            new_file_path = '%s/%s.%s' % (film.folder, film.id, film.file.type)
            if not os.path.exists(new_file_path):
                # 移动文件
                shutil.move(film.file.path, new_file_path)

    def create_folder(self):
        folder = os.path.join(self.__film__.file.path, self.__film__.title)
        if not os.path.exists(folder):
            Path(folder).mkdir(exist_ok=True)

    def save_poster(self, request):
        print("封面下载")
        TaskPool.append_task(Task(__save_image__, [self.__film__.poster, request]))
        # __save_image__([self.__film__.poster, request])

    def save_stills(self, request):
        print("剧照下载")
        if self.__film__.stills is not None and len(self.__film__.stills) > 0:
            tasks = [Task(__save_image__, [still, request]) for still in self.__film__.stills]
            TaskPool.append_tasks(tasks)

            # thread_pool = ThreadPool(tasks)
            # thread_pool.execute()

    def __save_information_file__(self, args):
        print("保存信息文件")
        source = args["source"]
        file_name = args["file_name"]

        if not os.path.exists(self.__film__.folder):
            Path(self.__film__.folder).mkdir(exist_ok=True)

            with open(os.path.join(self.__film__.folder, file_name), 'w', encoding='utf-8') as json_file:
                json.dump(source, json_file, indent=4, ensure_ascii=False)

    def save_information(self, source, file_name):
        TaskPool.append_task(Task(self.__save_information_file__, {"source": source, "file_name": file_name}))

    def save_torrents(self, request, save_info=False):
        print("种子下载")
        if self.__film__.torrents is not None and len(self.__film__.torrents) > 0:
            if save_info is True:
                if not os.path.exists(self.__film__.folder):
                    Path(self.__film__.folder).mkdir(exist_ok=True)

                with open(os.path.join(self.__film__.folder, 'torrent.json'), 'w', encoding='utf-8') as json_file:
                    json.dump(self.__film__.torrents, json_file, indent=4, ensure_ascii=False)

            tasks = [Task(__save_image__, [torrents, request]) for torrents in self.__film__.torrents]
            TaskPool.append_tasks(tasks)

            # thread_pool = ThreadPool(tasks)
            # thread_pool.execute()

    def scan_directory(self):
        if self.__film__.id:
            uid = self.__film__.id
        else:
            uid = self.__film__.title

        return dictionary.exists(uid)

    def append_to_dictionary(self):
        film = self.__film__
        excluded_types = ['torrent', 'jpg', 'png', 'gif']

        if film.file.type is not None and film.file.type not in excluded_types:
            print('写入字典')
            # dictionary.add(film.file)
