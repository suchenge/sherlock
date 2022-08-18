import os

import modules.av.collate.marauder.marauder_factory
import modules.av.collate.porter
import modules.av.dictionary
from modules.http_request.request import Request
from modules.http_request.proxy import Proxies
from modules.av.collate.file import File
from modules.av.collate.thread_pool import ThreadPool


class Collator(object):
    def __init__(self, path):
        self.__files__ = []

        if os.path.isfile(path):
            self.__files__.append(File(path))
        else:
            self.__files__ = [File(os.path.join(path, file_name)) for file_name in os.listdir(path)]

        self.__proxies__ = Proxies()
        self.__request__ = Request(self.__proxies__)

    def __neaten__(self, file):
        print("开始处理文件：" + file.path)
        print(' name：%s\n type：%s\n title：%s\n folder：%s\n path：%s\n'
              % (file.name, file.type, file.title, file.folder, file.path))

        if file.type == 'torrent' and modules.av.dictionary.exists(file.title):
            pass
        else:
            try:
                marauder = modules.av.collate.marauder.marauder_factory.get_marauder(file, self.__request__)
                film = marauder.to_film()

                print('文件解析结果\n id:%s\n title:%s\n posters:%s\n stills:\n%s\n'
                      % (film.id, film.title, film.poster['url'], '\n'.join(['       ' + stills['url'] for stills in film.stills])))

                porter = modules.av.collate.porter.Porter(film)
                porter.move()
                porter.save_poster(self.__request__)
                porter.save_stills(self.__request__)
                porter.append_to_dictionary()

            except Exception as error:
                print("处理出错:")
                print(error)

        print("处理文件完成 " + file.path)

    def run(self):
        tasks = [{'executor': self.__neaten__, 'args': file} for file in self.__files__]
        thread_pool = ThreadPool(tasks)
        thread_pool.execute()

        print('全部完成')
        self.__proxies__.close()
