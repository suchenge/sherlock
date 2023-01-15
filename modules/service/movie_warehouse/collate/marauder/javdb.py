from lxml import etree
from modules.service.movie_warehouse.collate.marauder.base import BaseMarauder, find_configuration_node
from modules.framework.configuration_manager.configuration_setting import configuration_setting


@configuration_setting('../../config/movie-website.json', False, 'url',
                       lambda json: find_configuration_node(json, 'default'))
class MarauderJavdb(BaseMarauder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__base_url__ = kwargs["url"]

        search_url = self.__base_url__ + 'search?q=' + self.__file__.title + '&f=all'
        html_content = self.__get_url_content__(search_url)

        if html_content is None:
            raise Exception("没有获取到页面内容")

        tree = etree.HTML(html_content)

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
                self.__content__ = self.__get_url_content__(self.__base_url__ + link)
                tree = etree.HTML(self.__content__)

                self.__id__ = uids[index]

                self.__title__ = tree.xpath("//span[@class='origin-title']/text()")[-1]
                if self.__title__ is None:
                    self.__title__ = tree.xpath("//strong[@class='current-title']/text()")[-1]

                self.__title__ = self.__id__ + " " + self.__title__

                self.__poster__ = tree.xpath("//img[@class='video-cover']/@src")[-1]
                self.__stills__ = tree.xpath("//div[@class='tile-images preview-images']/a[@class='tile-item']/@href")
        else:
            self.__content__ = None
