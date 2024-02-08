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
        if len(imgs) == 0:
            imgs = html.xpath("//p[@align='center']/img/@src")
        return [f'{self.__domain_url__}{item}' for item in imgs]

    def get_child_page_url(self):
        html_links = self.__html__.xpath("//div[@class='page']/a/@href")
        page_links = []

        for link in html_links:
            page_link = f'{self.__domain_url__}{link}'
            if page_link not in page_links:
                page_links.append(page_link)

        return page_links
