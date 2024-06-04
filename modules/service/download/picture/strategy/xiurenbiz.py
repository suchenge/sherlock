from modules.service.download.picture.strategy.base import Base

def build(url, html):
    return Xiurenbiz(url, html)


class Xiurenbiz(Base):
    def __init__(self, url, html):
        super().__init__(url, html)

    def get_title(self):
        title = self.__html__.xpath("//h1/text()")[-1]
        return title

    def get_images(self, html):
        result = html.xpath("//img[@decoding='async']/@src")
        result = [item for item in result if item.find('.webp') > -1]
        return result

    def get_child_page_url(self):
        return [self.__url__]