import os
import queue
import sys
import traceback

from pathlib import Path

from modules.framework.error_exception import ErrorException

from modules.service.movie_warehouse.collate.porter import Porter
from modules.service.movie_warehouse.collate.marauder import marauder_factory
from modules.service.movie_warehouse import dictionary
from modules.service.movie_warehouse.collate.file import File

from modules.tools.http_request.request import Request
from modules.tools.http_request.proxy import Proxies
from modules.tools.thread_pool import ThreadPool


class Collator(object):
    def __init__(self, path):
        self.__files__ = []
        self.__exceptions__ = queue.Queue()

        if os.path.isfile(path):
            self.__files__.append(File(path))
        else:
            self.__files__ = [File(os.path.join(path, file_name)) for file_name in os.listdir(path)]

        self.__proxies__ = Proxies(**{})
        self.__request__ = Request(self.__proxies__)

    def __neaten__(self, file):
        print("开始处理文件：" + str(file))
        if file.type == 'torrent' and dictionary.exists(file.title):
            os.remove(file.path)
        else:
            film = None
            try:
                marauder = marauder_factory.get_marauder(**{'file': file, 'request': self.__request__})
                film = marauder.to_film()

                print('文件解析结果\n %s' % str(film))

                porter = Porter(film)
                porter.move()
                porter.save_poster(self.__request__)
                porter.save_stills(self.__request__)
                porter.append_to_dictionary()

            except Exception as error:
                self.__exceptions__.put(ErrorException(error, file))
                try:
                    if file is not None and file.type == 'torrent':
                        exception_path = str.replace(file.path, file.type, 'exception.' + file.type)
                        os.rename(file.path, exception_path)

                        if film is not None:
                            if os.path.exists(film.folder):
                                Path(film.folder).rmdir()

                except Exception as error1:
                    self.__exceptions__.put(ErrorException(error, file))

        print("处理文件完成 " + file.path)

    def run(self):
        tasks = [{'executor': self.__neaten__, 'args': file} for file in self.__files__]
        thread_pool = ThreadPool(tasks)
        thread_pool.execute()

        self.__proxies__.close()

        has_errors = not self.__exceptions__.empty()
        while not self.__exceptions__.empty():
            e = self.__exceptions__.get()
            print(str(e))

        if has_errors:
            os.system("pause")
        else:
            print('全部完成')
