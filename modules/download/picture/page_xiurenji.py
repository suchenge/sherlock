import re

from modules.download.picture.page_base import PageBase


class PageXiuRenJi(PageBase):
    def __init__(self, url):
        super().__init__(url)
        self.charset = "gb18030"

    def get_title(self, page_content):
        regex = re.compile('<div class=title>(.*?)</div>', re.DOTALL)
        result = re.findall(regex, page_content)[0]
        return result.replace("\r", "").replace("\n", "")
