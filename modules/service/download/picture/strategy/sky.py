from modules.tools.common_methods.unity_tools import get_file_suffix
from modules.service.download.picture.strategy.base import Base


class Sky(Base):
    def __init__(self, url, html):
        super().__init__(url, html)

    @staticmethod
    def is_match(url, html):
        return url.find('186sky') > -1

    def get_title(self):
        title = self.__html__.xpath('//h1')
        title = title[0].text
        return title

    def get_child_page_url(self):
        pages = self.__html__.xpath("//div[@class='scroll-content']/a/@href")
        pages = [{'index': index + 1, 'url': f'{self.__domain_url__ + item}'} for index, item in enumerate(pages)]
        return pages

    def get_images(self, html, page_index=None):
        pictures = html.xpath("//img[@class='lazy']/@data-original")
        result = [{"name": f'{str(page_index).zfill(5)}.{str(index).zfill(5)}.{get_file_suffix(pic)}', "url": pic} for index, pic in enumerate(pictures)]
        return result
