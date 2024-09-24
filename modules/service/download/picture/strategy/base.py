import os
import concurrent.futures

from pathlib import Path
from lxml import etree

from modules.service.download.picture.saver.database import DatabaseSaver
from modules.service.download.picture.image import Image
from modules.service.download.picture.page import Page


from modules.tools.common_methods.unity_tools import parse_url, format_title
from modules.tools.http_request.request import Request


class Base(object):
    def __init__(self, url):
        self.__url__ = url
        self.__title__ = None

        self.__open_saver__ = self.__inner_open_saver__()
        self.__has_by_saver__ = False
        self.__images_by_saver__: None | list[Image]
        self.__saver__ = self.__get_by_saver__()
        self.__request__ = self.__inner_get_request__()

        if not self.__has_by_saver__:
            self.__domain_url__, self.__url_path__ = parse_url(url)

            self.__html__ = self.get_tree(url)

    def __get_by_saver__(self) -> None | DatabaseSaver:
        if self.__open_saver__:
            saver = DatabaseSaver()
            save_images = saver.query(self.__url__)

            self.__images_by_saver__ = save_images
            self.__has_by_saver__ = save_images is not None and len(save_images) > 0

            return saver

    def __inner_open_saver__(self):
        return False

    def __insert_images_by_saver__(self, images: list[Image]):
        if self.__open_saver__ and len(images) > 0:
            self.__saver__.insert_by_batch(images)

    def __insert_image_by_saver__(self, image: Image):
        if self.__open_saver__:
            self.__saver__.insert(image)

    def __delete_image_by_url__(self, url: str):
        if self.__open_saver__:
            self.__saver__.delete(url)

    def delete_image_by_urls(self, url: list[str]):
        if self.__open_saver__ and len(url) > 0:
            self.__saver__.delete_batch(url)

    @staticmethod
    def is_match(url) -> bool:
        return False

    @property
    def html(self):
        return self.__html__

    def __inner_get_request__(self) -> Request:
        return Request()

    def __inner_get_title__(self) -> str:
        pass

    def __inner_get_sub_page_url__(self) -> list[str]:
        pass

    def __inner_get_images__(self, html_tree) -> list[str]:
        pass

    def __inner_get_sub_page_title__(self, html_tree=None) -> str:
        return ''

    def __build_sub_page__(self, page_info):
        page = Page()
        page.url = page_info['url']
        page.index = page_info['index']
        page.html = self.get_tree(page.url)
        page.title = self.__inner_get_sub_page_title__(page.html)
        return page

    def __get_sub_page__(self) -> list[Page]:
        page_urls = self.__inner_get_sub_page_url__()

        if len(page_urls) > 0 and page_urls[0] != self.__url__:
            page_infos = [{'url': item, 'index': index} for index, item in enumerate(page_urls)]

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                pages = executor.map(self.__build_sub_page__, page_infos)
        else:
            page = Page()
            page.url = page_urls[0]
            page.index = 0
            page.html = self.__html__
            page.title = self.__title__

        return list(pages)

    def __get_images_sub_page__(self, page) -> list[Image]:
        image_urls = self.__inner_get_images__(page.html)
        result = []

        index = 0
        for image_url in image_urls:
            image = Image(image_url)
            image.file_name = f'{str(index).zfill(5)}.{image.suffix}'

            if page.url != self.__url__:
                image.file_name = f'{str(page.index).zfill(5)}.{image.file_name}'

            image.main_title = self.__title__
            image.main_url = self.__url__
            image.sub_url = page.url
            image.sub_title = self.__inner_get_sub_page_title__()
            index += 1

            result.append(image)

        return result

    def get_title(self):
        if self.__title__:
            return self.__title__

        if self.__has_by_saver__:
            self.__title__ = self.__images_by_saver__[0].main_title
        else:
            self.__title__ = self.__inner_get_title__()
            self.__title__ = format_title(self.__title__)

        return self.__title__

    def get_images(self):
        if self.__has_by_saver__:
            return self.__images_by_saver__
        else:
            result = []
            sub_page = self.__get_sub_page__()

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                page_images = executor.map(self.__get_images_sub_page__, sub_page)

                for images in page_images:
                    for image in images:
                        result.append(image)

            self.__insert_images_by_saver__(result)
            return result

    def get_html(self, url):
        return self.__request__.get_text(url)

    def get_tree(self, url):
        html = self.get_html(url)
        return etree.HTML(html)

    def download_image(self, **kwargs) -> None | str:
        path = kwargs["path"]
        url = kwargs["url"]

        if os.path.exists(path):
            return url

        print(kwargs)

        if path and url:
            content = self.__request__.get_content(url)

            if content:
                folder = os.path.dirname(path)

                if not os.path.exists(folder):
                    Path(folder).mkdir(exist_ok=True)

                with open(path, "ab") as file:
                    file.write(content)

                self.__delete_image_by_url__(url)
                return url
            else:
                print(f'图片[{url}]下载出错')
                return None


