from modules.service.download.picture.strategy.base import Base


class Xiurenbiz(Base):
    def __init__(self, url):
        super().__init__(url)

    @staticmethod
    def is_match(url):
        return url.find('xiuren.biz') > -1

    def get_title(self):
        title = self.__html__.xpath("//h1/text()")[-1]
        return title

    def get_images(self, html, page_index=None):
        result = html.xpath("//img[@decoding='async']/@src")
        result = [item for item in result if item.find('.webp') > -1]
        return result

    def get_child_page_url(self):
        return [self.__url__]
