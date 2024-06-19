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
        pages = self.__html__.xpath("//div[@class='scroll-content']/a/@href")
        base_url = self.__parse_url__()
        pages = [f'{base_url[0] + item}' for item in pages]
        return pages

    def get_images(self, html):
        return html.xpath("//img[@class='lazy']/@data-original")
