import re

from modules.service.download.picture.page_base import PageBase


class PageXinannvku(PageBase):
    def __init__(self, url):
        super().__init__(url)

    def get_title(self, page_content):
        result = re.findall('<h1>(.*?)</h1>', page_content)[0]
        return result

    def get_picture_list(self, page_content):
        regex = re.compile('<img src="(.*?)".*class="content_img".*?>')
        result = re.findall(regex, page_content)
        return result

    def get_other_page_list(self, page_content):
        url_template = self.url.replace("-1.html", "")
        url_regex = url_template + "-\\d+." + "html"
        other_url_list = re.findall(url_regex, page_content)
        max_url = other_url_list[len(other_url_list) - 2]
        re_mathcer = re.findall(re.compile('(\\d+).html'), max_url)
        max_index = re_mathcer[0]
        max_index_num = 1 + int(max_index)
        result = []
        for index in range(2, max_index_num):
            result.append(url_template + "-" + str(index) + ".html")
        return result