from re import findall
from download.picture.page_base import PageBase


class PageJpmnb(PageBase):
    def __init__(self, url):
        super().__init__(url)

    def get_title(self):
        result = findall('<div class=\"title\">(.*?)</div>', self.page_content)
        return result

    def get_picture_list(self):
        return findall('<img onload="size\(this\)" .*? src="(.*?)".*?>', self.page_content)
