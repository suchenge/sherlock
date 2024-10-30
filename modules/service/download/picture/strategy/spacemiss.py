from modules.service.download.picture.strategy.proxy_base import ProxyBase


class Spacemiss(ProxyBase):
    def __init__(self, url):
        super().__init__(url)

    @staticmethod
    def is_match(url):
        return url.find('spacemiss') > -1

    def __inner_get_title__(self):
        title = self.__html__.xpath("//h1[@class='tdb-title-text']")
        title = title[0].text
        #title = title.split('-')[0].strip().replace('|', '')
        return title

    def __inner_get_images__(self, html_tree):
        return html_tree.xpath("//img[@decoding='async']/@src")

    def __inner_get_sub_page_url__(self):
        return [self.__url__]
