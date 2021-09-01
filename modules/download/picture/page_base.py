import os
import zipfile
import wget
import ssl
import re

import concurrent.futures

from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse


class PageBase(object):
    __threadCount = 10

    def __init__(self, url):
        self.url = url
        self.domain_url, self.url_path = self.__parse_url()
        self.charset = "utf-8"

    def __parse_url(self):
        url_info = urlparse(self.url)
        return url_info.scheme + "://" + url_info.netloc, url_info.path

    def __get_picture_suffix(self, picture_url):
        picture_name = os.path.split(picture_url)[-1]
        picture_suffix = picture_name.split(".")[-1]
        return picture_suffix

    def __get_picture_list(self, page_url):
        page_content = self.get_page_content(self.domain_url + page_url)
        picture_list = self.get_picture_list(page_content)
        return picture_list

    def __download(self, picture):
        key, value = picture
        wget.download(key, value)

    def get_title(self, page_content):
        pass

    def get_picture_list(self, page_content):
        regex = re.compile('<img onload="size\(this\)" .*? src="(.*?)".*?>', re.DOTALL)
        result = re.findall(regex, page_content)
        return result

    def get_other_page_list(self, page_content):
        url_path_list = self.url_path.split(".")
        url_regex = url_path_list[0] + "_\\d+." + url_path_list[1]
        other_url_list = re.findall(url_regex, page_content)
        result = list(set(other_url_list))
        result.sort(key=other_url_list.index)
        return result

    def get_page_content(self, page_url):
        page_content = urlopen(page_url, context=ssl._create_unverified_context()).read()
        page_content = page_content.decode(self.charset)
        return page_content

    def download(self, download_folder):
        # 当前页面html
        page_content = self.get_page_content(self.url)
        # 当前页面Title
        title = self.get_title(page_content)
        # 当前页面的Picture List
        picture_list = self.get_picture_list(page_content)
        # 当前页面的子页面
        other_page_list = self.get_other_page_list(page_content)

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__threadCount) as executor:
            other_page_picture_list = executor.map(self.__get_picture_list, other_page_list)

        for other_picture_list in other_page_picture_list:
            picture_list.extend(other_picture_list)

        picture_folder = download_folder + "/" + title
        Path(picture_folder).mkdir(exist_ok=True)

        picture_dict = []
        for index in range(len(picture_list)):
            picture_url = self.domain_url + picture_list[index]
            picture_path = picture_folder + "/" + str(index).zfill(5) + "." + self.__get_picture_suffix(picture_url)
            picture_dict.append((picture_url, picture_path))

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__threadCount) as executor:
            executor.map(self.__download, picture_dict)

        # self.__to_zip(picture_folder)

    def __to_zip(self, picture_folder):
        zip_file = picture_folder + ".zip"
        zip = zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED)

        for dirpath, dirnames, filenames in os.walk(picture_folder):
            file_path = dirpath.replace(picture_folder, "")
            file_path = file_path and file_path + os.sep or ''

            for file_name in filenames:
                zip.write(os.path.join(dirpath, file_name), file_path + file_name)

        zip.close()
