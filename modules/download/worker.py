import os
import concurrent.futures

from modules.download.picture.page_url import PageUrl
from modules.download.picture.page_factory import PageFactory


class Worker(object):
    def __init__(self):
        self.__threadCount = 5
        self.xml_path = os.path.abspath("data/source/picture.xml")
        self.download_folder = os.path.abspath("data/download")
        self.page_url = PageUrl(self.xml_path)

    def __download(self, url):
        page_instance = PageFactory.get_instance(url)(url)
        page_instance.download(self.download_folder)
        self.page_url.done(url)

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__threadCount) as executor:
            executor.map(self.__download, self.page_url.items)