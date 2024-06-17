from lxml import etree

from modules.tools.http_request.http_client import HttpClient
from modules.service.download.cartoon.strategy.base import BaseCartoonStrategy

class SkyCartoonStrategy(BaseCartoonStrategy):
    def __init__(self, url):
        super().__init__(url)

    @staticmethod
    def is_match(url):
        return url.find('186sky') > -1

    def get_title(self):
        title = self.__html__.xpath('//h1')
        title = title[0].text
        return title

    def get_image(self):
        pages = self.__html__.xpath("//div[@class='scroll-content']/a/@href")
        base_url = self.__parse_url__()
        pages = [f'{base_url[0] + item}' for item in pages]

        index = 1
        result = []
        for page in pages:
            page_content = HttpClient.get_text(page)
            page_html = etree.HTML(page_content)
            title = page_html.xpath("//h2/text()")[0]
            pictures = page_html.xpath("//img[@class='lazy']/@data-original")

            for picture in pictures:
                result.append({"name": str(index).zfill(5), "url": picture})

        return result

