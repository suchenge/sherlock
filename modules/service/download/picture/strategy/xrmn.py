from modules.service.download.picture.strategy.base import Base

def build(url, html):
    return Xrmn(url, html)
class Xrmn(Base):
    def __init__(self, url, html):
        super().__init__(url, html)

    def get_title(self):
        title = self.__html__.xpath("//h1/text()")[-1]
        return title

    def get_images(self, html):
        imgs = html.xpath("//p[@style='text-align: center']/img/@src")
        return [f'{self.__domain_url__}{item}' for item in imgs]

    def get_child_page_url(self):
        html_links = self.__html__.xpath("//div[@class='page']/a[not(contains(@class, 'current'))]/@href")
        page_links = []

        for link in html_links:
            if link not in page_links and link not in self.__url__:
                page_links.append(f'{self.__domain_url__}{link}')

        return page_links
