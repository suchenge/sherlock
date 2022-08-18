import os
import queue

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
        print("开始处理文件：" + file.path)
        print(' name：%s\n type：%s\n title：%s\n folder：%s\n path：%s\n'
              % (file.name, file.type, file.title, file.folder, file.path))

        if file.type == 'torrent' and dictionary.exists(file.title):
            pass
        else:
            try:
                marauder = marauder_factory.get_marauder(**{'file': file, 'request': self.__request__})
                film = marauder.to_film()

                print('文件解析结果\n id:%s\n title:%s\n posters:%s\n stills:\n%s\n'
                      % (film.id, film.title, film.poster['url'],
                         '\n'.join(['       ' + stills['url'] for stills in film.stills])))

                porter = Porter(film)
                porter.move()
                porter.save_poster(self.__request__)
                porter.save_stills(self.__request__)
                porter.append_to_dictionary()

            except Exception as error:
                self.__exceptions__.put(error)

        print("处理文件完成 " + file.path)

    def run(self):
        tasks = [{'executor': self.__neaten__, 'args': file} for file in self.__files__]
        thread_pool = ThreadPool(tasks)
        thread_pool.execute()

        self.__proxies__.close()

        has_errors = not self.__exceptions__.empty()
        while not self.__exceptions__.empty():
            print(self.__exceptions__.get())

        if has_errors:
            os.system("pause")
        else:
            print('全部完成')

