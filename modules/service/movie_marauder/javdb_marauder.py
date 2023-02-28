import os
from lxml import etree

from modules.tools.http_request.http_client import HttpClient
from modules.service.movie_marauder.base_marauder import BaseMarauder, find_configuration_node, build_torrent_url
from modules.framework.configuration_manager.configuration_setting import configuration_setting


@configuration_setting('../../config/movie-website.json', False, 'url',
                       lambda json: find_configuration_node(json, 'default'))
class JavdbMarauder(BaseMarauder):
    def __init__(self, **kwargs):
        super().__init__()

        self.__base_url__ = kwargs["url"]
        self.__id__ = None
        self.__title__ = None

    def search(self, key: str) -> str:
        result = None

        try:
            search_url = "%ssearch?q=%s&f=all" % (self.__base_url__, key)

            html_content = HttpClient.get_text(search_url)
            tree = etree.HTML(html_content)
            links = tree.xpath("//div[@class='item']/a/@href")
            uids = tree.xpath("//div[@class='video-title']/strong/text()")

            if 0 < len(links) == len(uids) > 0:
                index = 0

                if key in uids:
                    index = uids.index(key)
                else:
                    for i in range(len(uids)):
                        if uids[i] in key:
                            index = i
                            break

                if index > -1:
                    result = links[index]
        finally:
            return result

    def is_match(self, url: str) -> bool:
        if self.__base_url__ in url:
            return True
        else:
            return False

    def __get_id__(self):
        if self.__id__ is None or self.__id__ == "":
            pass

        return self.__id__

    def __get_title__(self):
        if self.__title__ is None or self.__title__ == "":
            element = self.__html_content__.xpath("//span[@class='origin-title']/text()")

            if element is None or len(element) >= 0:
                element = self.__html_content__.xpath("//strong[@class='current-title']/text()")

            if element:
                self.__title__ = self.__get_id__() + "" + element[-1]

        return self.__title__

    def __get__poster__(self) -> {}:
        poster = self.__html_content__.xpath("//img[@class='video-cover']/@src")[-1]
        if poster:
            return {
                "name": self.__get_id__() + os.path.splitext(poster)[-1],
                "url": poster
            }

    def __get_stills__(self) -> [{}]:
        result = []
        still_hrefs = self.__html_tree__.xpath("//div[@class='tile-images preview-images']/a[@class='tile-item']/@href")
        if still_hrefs and len(still_hrefs) > 0:
            for index in range(0, len(still_hrefs)):
                url = still_hrefs[index]
                name = os.path.split(url)[-1]
                type = name.split(".")[-1]

                result.append({
                    "name": "%s_%s.%s" % (self.__get_id__(), index, type),
                    "url": url
                })

        return result

    def __get_torrents__(self) -> [{}]:
        result = []
        magent_links = self.__html_tree__.xpath("//div[@id='magnets-content']")[-1]
        if magent_links is not None and len(magent_links) > 0:
            index = 0
            for link in magent_links:
                index = index + 1
                info = link.getchildren()[0].find("a")
                url = info.get("href")
                size = info.getchildren()[2].text.strip()
                result.append({
                    "url": build_torrent_url(url),
                    "link": url,
                    "name": self.__get_id__() + '_' + str(index) + '_' + size + '.torrent'
                })

        return result

