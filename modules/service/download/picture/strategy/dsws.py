import os

from pathlib import Path
from playwright.sync_api import ProxySettings, sync_playwright

from modules.service.download.picture.image import Image
from modules.tools.common_methods.unity_tools import format_title
from modules.tools.http_request.proxy import Proxies
from modules.tools.http_request.request import Request


class Dsws(object):
    def __init__(self, url):
        self.__url__ = url
        self.__images__ = []
        self.__title__ = None

        self.__request__ = Request(Proxies(), True)

        home_url = r'https://dsws.ok3753682.com/'
        proxy_setting = {
            'server': f'https://{Proxies().get().proxy_address}',
            'username': 'suchenge',
            'password': 'suyuan2UnionPay',
        }

        proxy_settings = ProxySettings(proxy_setting)

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True, proxy=proxy_settings)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            page.goto(home_url)
            page.locator("//p[@class='enter-btn']").first.click()
            page.goto(self.__url__)

            self.__title__ = page.locator("//h1[@id='subject_tpc']").inner_text()
            self.__title__ = format_title(self.__title__)

            images = page.locator("//img[@class='preview-img']").all()

            index = 0
            for image in images:
                index = index + 1
                url = image.get_attribute("data-original")
                image_item = Image(url)
                image_item.file_name = f'{str(index).zfill(5)}.{image_item.suffix}'

                self.__images__.append(image_item)

    @staticmethod
    def is_match(url):
        return url.find('dsws') > -1

    def get_title(self):
        return self.__title__

    def get_images(self):
        return self.__images__

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

                return url
            else:
                print(f'图片[{url}]下载出错')
                return None
        return None


