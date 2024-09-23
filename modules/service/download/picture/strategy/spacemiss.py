from modules.service.download.picture.strategy.proxy_base import ProxyBase


class Spacemiss(ProxyBase):
    def __init__(self, url):
        super().__init__(url)

    @staticmethod
    def is_match(url):
        return url.find('spacemiss') > -1

    def __inner_get_title__(self):
        title = self.__html__.xpath("//title")
        title = title[0].text
        title = title.split('-')[0].strip().replace('|', '')
        return title

    def __inner_get_images_by_sub_page__(self, html, page_index=None):
        return html.xpath("//img[@decoding='async']/@src")

    def __inner_get_sub_page_url__(self):
        return [self.__url__]
