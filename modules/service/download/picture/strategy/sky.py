from modules.service.download.picture.strategy.base import Base

from modules.tools.http_request.proxy import Proxies
from modules.tools.http_request.request import Request

class Sky(ProxyBase):
    def __init__(self, url):
        super().__init__(url)

    def __inner_open_saver__(self):
        return True

    @staticmethod
    def is_match(url):
        return url.find('186sky') > -1

    def __inner_get_title__(self):
        title = self.__html__.xpath('//h1')
        title = title[0].text
        return title

    def __inner_get_sub_page_url__(self):
        pages = self.__html__.xpath("//div[@class='scroll-content']/a/@href")
        return [f'{self.__domain_url__}{item}' for index, item in enumerate(pages)]

    def __inner_get_images__(self, html_tree):
        return html_tree.xpath("//img[@class='lazy']/@data-original")

