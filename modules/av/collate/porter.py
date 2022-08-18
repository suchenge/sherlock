import os
import shutil

from pathlib import Path
from modules.av import dictionary
from modules.av.collate.thread_pool import ThreadPool


def __save_image__(args):
    image = args[0]
    request = args[1]

    path = image['path']
    url = image['url']

    content = request.get(url).content
    with open(path, "ab") as fs:
        fs.write(content)


class Porter(object):
    def __init__(self, film):
        self.__film__ = film

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

    def save_poster(self, request):
        print("封面下载")
        __save_image__([self.__film__.poster, request])

    def save_stills(self, request):
        print("剧照下载")
        if self.__film__.stills is not None and len(self.__film__.stills) > 0:
            tasks = [{'executor': __save_image__, 'args': [still, request]} for still in self.__film__.stills]

            thread_pool = ThreadPool(tasks)
            thread_pool.execute()

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
            dictionary.add(self.__film__.id, self.__film__.folder)
