from modules.service.download.picture.strategy.base import Base

def build(url, html):
    return Xinannvku(url, html)

class Xinannvku(Base):
    def __init__(self, url, html):
        super().__init__(url, html)

    def get_title(self):
        return self.__html__.xpath("//meta[@name='description']/@content")[0]

    def get_images(self, html):
        title = self.get_title()
        images = html.xpath("//img[contains(@title, '" + title + "')]/@src")
        return images

    def get_child_page_url(self):
        page_links = self.__html__.xpath("//div[@class='page']/a[not(contains(@class, 'current'))]/@href")
        return page_links
