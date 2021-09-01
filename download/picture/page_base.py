import abc
import wget
import ssl

from os.path import abspath
from urllib.request import urlopen
from urllib.parse import urlparse


class PageBase(metaclass=abc.ABCMeta):
    def __init__(self, url):
        self.url = url
        self.domain_url = self.get_domain_url()
        self.page_content = self.get_page_content()

    @abc.abstractmethod
    def get_title(self):
        pass

    @abc.abstractmethod
    def get_picture_list(self):
        pass

    def get_domain_url(self):
        domain_url = urlparse(self.url)
        return domain_url.scheme + "://" + domain_url.netloc + "/"

    def get_page_content(self):
        context = ssl._create_unverified_context()
        page_content = urlopen(self.url, context=context).read()
        page_content = page_content.decode("utf-8")
        return page_content

    def download(self):
        title = self.get_title()
        picture_list = self.get_picture_list()
        for index in range(len(picture_list)):
            picture_url = self.domain_url + picture_list[index]
            picture_path = abspath("/download_data/" + title) + str(index).zfill(5)
            wget.download(picture_url, picture_path)
