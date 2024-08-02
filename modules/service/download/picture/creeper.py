import os

from modules.service.download.picture.url_container import UrlContainer
from modules.service.download.picture.processor import Processor


class Creeper(object):
    def __init__(self):
        source_url_path = os.path.abspath("../data/picture_url/new.txt")
        done_url_path = os.path.abspath("../data/picture_url/done.txt")
        save_path = os.path.abspath("../data/picture_url/download/")

        self.__done_url_container__ = UrlContainer(done_url_path)
        self.__source_url_container__ = UrlContainer(source_url_path, True)

        self.__processor_list__ = [Processor(item, save_path) for item in self.__source_url_container__.items()]

        self.__deduplication__()

    def __download__(self, processor):
        processor.download()

    def __deduplication__(self):
        done_items = self.__done_url_container__.items()
        processors = []

        for processor in self.__processor_list__:
            if processor.url not in done_items:
                processors.append(processor)
            else:
                self.__source_url_container__.remove(processor.url)

        self.__source_url_container__.write()
        self.__processor_list__ = processors

    def run(self):
        for processor in self.__processor_list__:
            try:
                processor.download()

                self.__done_url_container__.append(processor.url, auto_write=True)
                self.__source_url_container__.remove(processor.url, auto_write=True)
            except Exception as error:
                print(f'error:{processor.url}')

