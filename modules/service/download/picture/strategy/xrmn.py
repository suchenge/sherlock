from modules.service.download.picture.strategy.base import Base

def build(url, html):
    return Xrmn(url, html)
class Xrmn(Base):
    def __init__(self, url, html):
        super().__init__(url, html)

    def get_title(self):
        title = self.__html__.xpath("//h1/text()")[-1]
        return title

    def get_images(self):
        title = self.get_title()
        imgs = self.__html__.xpath("//img[contains(@alt, '" + title + "')]/@src")
        return imgs

    def get_child_page_url(self):
        return self.__html__.xpath("//div[@class='page']/a[not(contains(@class, 'current'))]/@href")