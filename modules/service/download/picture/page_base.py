import os
import time
import zipfile
import wget
import ssl
import re

import concurrent.futures

from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse

from lxml import etree


class PageBase(object):
    __thread_count__ = 10
    __try_count__ = 5

    def __init__(self, url):
        self.url = url
        self.domain_url, self.url_path = self.__parse_url__()
        self.charset = "utf-8"
        self.__page_html__ = None
        self.__error_pictures__ = []

    def __parse_url__(self):
        url_info = urlparse(self.url)
        return url_info.scheme + "://" + url_info.netloc, url_info.path

    def __get_picture_suffix__(self, picture_url):
        picture_name = os.path.split(picture_url)[-1]
        picture_suffix = picture_name.split(".")[-1]
        return picture_suffix

    def __get_picture_list__(self, page_url):
        url = page_url
        if "http" not in page_url:
            url = self.domain_url + "/" + page_url

        page_content = self.get_page_content(url)
        picture_list = self.get_picture_list(page_content)
        return picture_list

    def __append_error_picture__(self, picture):
        picture_key, picture_value = picture
        if len(self.__error_pictures__) <= 0:
            self.__error_pictures__.append((picture_key, picture_value, 0))
        else:
            error_index = -1
            for error_key, error_value, error_try_count in self.__error_pictures__:
                error_index += 1
                if error_key == picture_key:
                    error_try_count += 1
                    if error_try_count > 3:
                        self.__error_pictures__.remove(error_index)
                else:
                    self.__error_pictures__.append((picture_key, picture_value, 0))

    def __download__(self, picture, try_count=0):
        key, value = picture
        if not os.path.exists(value):
            try:
                print('下载请求[%s]：%s' % try_count if try_count < 5 else 'end', key)
                wget.download(key, value)
            except Exception as e:
                if try_count < 5:
                    try_count += 1
                    time.sleep(3)
                    self.__download__(picture, try_count)

    def get_title(self, page_content):
        result = re.findall('<h1 class=\"article-title\">(.*?)</h1>', page_content)[0]
        return result

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
        self.__page_html__ = etree.HTML(page_content)
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

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__thread_count__) as executor:
            other_page_picture_list = executor.map(self.__get_picture_list__, other_page_list)

        for other_picture_list in other_page_picture_list:
            picture_list.extend(other_picture_list)

        effective_picture_list = []
        for picture in picture_list:
            if picture not in effective_picture_list:
                effective_picture_list.append(picture)

        picture_folder = download_folder + "/" + title
        Path(picture_folder).mkdir(exist_ok=True)

        picture_dict = []
        for index in range(len(effective_picture_list)):
            picture_url = effective_picture_list[index]
            if "http" not in picture_url:
                picture_url = self.domain_url + picture_url

            picture_path = picture_folder + "/" + str(index).zfill(5) + "." + self.__get_picture_suffix__(picture_url)
            picture_dict.append((picture_url, picture_path))

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.__thread_count__) as executor:
            executor.map(self.__download__, picture_dict)

        return picture_folder
