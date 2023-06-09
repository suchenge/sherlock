from urllib.parse import \
    urlparse


class Base(object):
    def __init__(self, url, html):
        self.__url__ = url
        self.__html__ = html
        self.__domain_url__, self.__url_path__ = self.__parse_url__()

    def __parse_url__(self):
        url_info = urlparse(self.__url__)
        return url_info.scheme + "://" + url_info.netloc, url_info.path

    def get_title(self):
        return self.__html__.xpath("//h1[@class='article-title']/text()")

    def get_child_page_url(self):
        url_path = self.__url__.split('.')
        return self.__html__.xpath(f"//a[contains(@href,'{url_path}')]/@href")

    def get_images(self, html):
        return [f'{self.__domain_url__}{item}' for item in html.xpath('img[@onload="size(this)"]/@src')]
