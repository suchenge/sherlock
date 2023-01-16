from modules.service.download.picture.page_base import PageBase


class PageXrmn(PageBase):
    def __init__(self, url):
        super().__init__(url)

    def get_title(self, page_content):
        title = self.__page_html__.xpath("//h1/text()")[-1]
        return title

    def get_picture_list(self, page_content):
        title = self.get_title(page_content)
        imgs = self.__page_html__.xpath("//img[contains(@alt, '" + title + "')]/@src")
        return imgs

    def get_other_page_list(self, page_content):
        page_links = self.__page_html__.xpath("//div[@class='page']/a[not(contains(@class, 'current'))]/@href")
        return page_links