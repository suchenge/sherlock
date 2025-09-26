from modules.tools.http_request.request import Request

from modules.service.download.picture.strategy.proxy_base import ProxyBase


class Meitu8(ProxyBase):
    def __init__(self, url):
        super().__init__(url)
        self.__base_url__ = url.replace('.html', '')

    def __inner_open_saver__(self):
        return True

    def __inner_get_request__(self):
        return Request(None, True)

    @staticmethod
    def is_match(url):
        return url.find('meitu8') > -1

    def __inner_get_title__(self):
        title = self.__html__.xpath('//h1')
        title = title[0].text
        return title

    def __inner_get_sub_page_url__(self):
        page_btn = self.__html__.xpath("//div[@class='small pagelist']/b")[0]
        page_max_index = int(page_btn.text.split('/')[1])
        pages = [f'{self.__base_url__ }_{item}.html' for item in range(1, page_max_index + 1)]
        pages[0] = f'{self.__base_url__ }.html'

        return pages

    def __inner_get_images__(self, html_tree):
        return html_tree.xpath("//article/img/@src")

