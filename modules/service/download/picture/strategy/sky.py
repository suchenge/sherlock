from lxml import etree

from modules.tools.http_request.http_client import HttpClient
from modules.service.download.picture.strategy.base import Base


class Sky(Base):
    def __init__(self, url, html):
        super().__init__(url, html)

    @staticmethod
    def is_match(url, html):
        return url.find('186sky') > -1

    def get_title(self):
        title = self.__html__.xpath('//h1')
        title = title[0].text
        return title

    def get_child_page_url(self):
        return [self.__url__]

    def get_images(self, html):
        pages = self.__html__.xpath("//div[@class='scroll-content']/a/@href")
        base_url = self.__parse_url__()
        pages = [f'{base_url[0] + item}' for item in pages]

        page_index = 0
        result = []

        for page in pages:
            page_index = page_index + 1
            page_content = HttpClient.get_text(page)
            page_html = etree.HTML(page_content)
            pictures = page_html.xpath("//img[@class='lazy']/@data-original")

            picture_index = 0
            for picture in pictures:
                picture_index = picture_index + 1
                result.append({"name": f'{str(page_index).zfill(5)}.{str(picture_index).zfill(5)}.{self.__get_picture_suffix__(picture)}', "url": picture})

        return result
