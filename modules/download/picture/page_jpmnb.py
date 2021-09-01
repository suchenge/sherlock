import re

from modules.download.picture.page_base import PageBase


class PageJpmnb(PageBase):
    def __init__(self, url):
        super().__init__(url)

    def get_title(self, page_content):
        result = re.findall('<h1 class=\"article-title\">(.*?)</h1>', page_content)[0]
        return result
