from modules.service.download.picture.strategy.proxy_base import ProxyBase


class Spacemiss(ProxyBase):
    def __init__(self, url, html):
        super().__init__(url, html)

    @staticmethod
    def is_match(url, html):
        return url.find('spacemiss') > -1

    def get_title(self):
        title = self.__html__.xpath("//title")
        title = title[0].text
        title = title.split('-')[0].strip().replace('|', '')
        return title

    def get_images(self, html, page_index=None):
        return html.xpath("//img[@decoding='async']/@src")

    def get_child_page_url(self):
        return [self.__url__]
