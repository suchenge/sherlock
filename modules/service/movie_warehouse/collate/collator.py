import os
import queue
import sys
import traceback

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
            os.remove(file.path)
        else:
            film = None
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
                try:
                    if file is not None and file.type == 'torrent':
                        exception_path = str.replace(file.path, file.type, 'exception.' + file.type)
                        os.rename(file.path, exception_path)

                        if film is not None:
                            if os.path.exists(film.folder):
                                os.remove(film.folder)

                except Exception as error1:
                    self.__exceptions__.put(error1)



        print("处理文件完成 " + file.path)

    def run(self):
        tasks = [{'executor': self.__neaten__, 'args': file} for file in self.__files__]
        thread_pool = ThreadPool(tasks)
        thread_pool.execute()

        self.__proxies__.close()

        has_errors = not self.__exceptions__.empty()
        while not self.__exceptions__.empty():
            e = self.__exceptions__.get()

            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))

            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." % (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())

        if has_errors:
            os.system("pause")
        else:
            print('全部完成')
