from modules.service.download.picture.page_base import PageBase


class PageXinannvku(PageBase):
    def __init__(self, url):
        super().__init__(url)

    def get_title(self, page_content):
        title = self.__page_html__.xpath("//h1/text()")[-1]
        return title

    def get_picture_list(self, page_content):
        result = self.__page_html__.xpath("//img[@class='content_img']/@src")
        return result

    def get_other_page_list(self, page_content):
        result = []
        url_template = self.url.replace("-1.html", "")
        page_links = self.__page_html__.xpath("//div[@id='pages']/a/text()")
        max_page_count = page_links[len(page_links) - 2]

        for index in range(2, int(max_page_count) + 1):
            result.append(url_template + "-" + str(index) + ".html")

        return result
