import os

from modules.service.movie_warehouse.collate.porter import Porter
from modules.service.movie_warehouse.collate.marauder import marauder_factory
from modules.service.movie_warehouse.collate import \
    dictionary
from modules.service.movie_warehouse.collate.file import File

from modules.tools.http_request.request import Request
from modules.tools.http_request.proxy import Proxies
from modules.tools.thread_pool import ThreadPool
from modules.tools.exception_container.exception_wrapper import exception_wrapper


def __torrent_neaten_error_handler__(error, *args, **kwargs):
    file = args[1]
    if file is not None and file.type == 'torrent':
        exception_path = str.replace(file.path, file.type, 'exception.' + file.type)
        os.rename(file.path, exception_path)

        # if film is not None:
        #     if os.path.exists(film.folder):
        #         Path(film.folder).rmdir()


@exception_wrapper()
class Collator(object):
    def __init__(self, path):
        self.__path__ = path
        self.__proxies__ = Proxies(**{})
        self.__request__ = Request(self.__proxies__)

    @exception_wrapper()
    def __build_files__(self):
        files = []

        if os.path.isfile(self.__path__):
            files.append(File(self.__path__))
        else:
            files = [File(os.path.join(self.__path__, file_name)) for file_name in os.listdir(self.__path__)]

        return files

    @exception_wrapper(record_exception_after_handler=__torrent_neaten_error_handler__)
    def __neaten__(self, file):
        if file is None:
            pass

        print("开始处理文件：" + str(file))

        if file.type == 'torrent' and dictionary.exists(file.title, file.path):
            os.remove(file.path)
        else:
            marauder = marauder_factory.get_marauder(**{'file': file, 'request': self.__request__})
            film = marauder.to_film()

            print('文件解析结果\n %s' % str(film))

            porter = Porter(film)
            porter.move()
            porter.save_poster(self.__request__)
            porter.save_stills(self.__request__)
            porter.append_to_dictionary()

        print("处理文件完成 " + file.path)

    def run(self):
        files = self.__build_files__()

        if files is not None:
            tasks = [{'executor': self.__neaten__, 'args': file} for file in files]
            thread_pool = ThreadPool(tasks, 10)
            thread_pool.execute()

        self.__proxies__.close()

        print('全部完成')

