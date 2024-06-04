from modules.service.download.picture.strategy.base import Base

def build(url, html):
    return Spacemiss(url, html)


class Spacemiss(Base):
    def __init__(self, url, html):
        super().__init__(url, html)

    def get_title(self):
        title = self.__html__.xpath("//title")
        title = title[0].text
        title = title.split('-')[0].strip().replace('|', '')
        return title

    def get_images(self, html):
        try:
            result = html.xpath("//img[@decoding='async']/@src")
            return result
        except Exception as error:
            print(error)

    def get_child_page_url(self):
        return [self.__url__]