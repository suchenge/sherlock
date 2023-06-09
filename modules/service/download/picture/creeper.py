import os
import concurrent.futures

from modules.service.download.picture.url_container import UrlContainer
from modules.service.download.picture.processor import Processor


class Creeper(object):
    def __init__(self):
        source_url_path = os.path.abspath("../data/picture_url/new.txt")
        done_url_path = os.path.abspath("../data/picture_url/done.txt")
        save_path = os.path.abspath("../data/picture_url/")

        self.__done_url_container__ = UrlContainer(done_url_path)
        self.__source_url_container__ = UrlContainer(source_url_path)

        self.__processor_list__ = [Processor(item, save_path) for item in self.__source_url_container__.items() if item not in self.__done_url_container__.items()]

    def __download__(self, processor):
        processor.download()

    def run(self):
        for processor in self.__processor_list__:
            try:
                processor.download()
                self.__done_url_container__.append(processor.url, auto_write=True)
                self.__source_url_container__.remove(processor.url, auto_write=True)
            except Exception as error:
                print(f'error:{processor.url}')

