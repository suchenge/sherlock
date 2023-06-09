import \
    re

from modules.service.download.picture.strategy.base import Base

def build(url, html):
    return Xiurenba(url, html)

class Xiurenba(Base):
    def __init__(self, url, html):
        super().__init__(url, html)

    def get_title(self):
        return self.__html__.xpath("//h1/text()")[-1]

    def get_images(self, html):
        return [f'{self.__domain_url__}{item}' for item in html.xpath("//div[@class='content']/p/img/@src")]

    def get_child_page_url(self):
        html_links = self.__html__.xpath("//div[@class='page']/a/@href")
        page_links = []

        for link in html_links:
            if link not in page_links and link not in self.__url__:
                page_links.append(link)

        return page_links
