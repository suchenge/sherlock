from lxml import etree

from modules.tools.http_request.request import Request

from modules.service.movie_library.archive.label import Label
from modules.service.movie_library.archive.analyzer.base import Analyzer


class Javdb(Analyzer):
    def __init__(self, request: Request):
        super().__init__(request)
        self.__base_url__ = 'https://javdb.com/'

    def create_label(self, uid: str) -> Label:
        search_url = f'{self.__base_url__}search?q={uid}&f=all'
        html_content = self.__get_url_content__(search_url)

        parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.HTML(html_content, parser)

        links = tree.xpath("//div[@class='item']/a/@href")
        uids = tree.xpath("//div[@class='video-title']/strong/text()")

        if 0 < len(links) == len(uids) > 0:
            index = 0
            if self.__file__.title in uids:
                index = uids.index(self.__file__.title)
            else:
                for i in range(len(uids)):
                    if uids[i] in self.__file__.title:
                        index = i
                        break
            if index > -1:
                link = links[index]
                return self.__build__(self.__base_url__ + link, uids[index])
        else:
            raise Exception("没有查询到档案信息")

    def __build__(self, link, uid) -> Label:
        result = Label()
        result.uid = uid

        content = self.__get_url_content__(link)

        parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.HTML(content, parser)

        title_element = tree.xpath("//span[@class='origin-title']/text()")
        if title_element is None or len(title_element) == 0:
            title_element = tree.xpath("//strong[@class='current-title']/text()")

        result.title = f'{id} {title_element[-1]}'

        result.poster = tree.xpath("//img[@class='video-cover']/@src")[-1]
        result.stills = tree.xpath("//div[@class='tile-images preview-images']/a[@class='tile-item']/@href")

        return result

