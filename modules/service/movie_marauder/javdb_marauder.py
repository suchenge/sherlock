import os

from modules.tools.http_request.request import Request
from modules.service.movie_marauder.base_marauder import BaseMarauder


class JavdbMarauder(BaseMarauder):
    def __init__(self, url: str, request: Request):
        super().__init__(url, request)

    def __get_id__(self) -> str:
        pass

    def __get_title__(self) -> str:
        pass

    def __get__poster__(self) -> {}:
        poster = self.__html_content__.xpath("//img[@class='video-cover']/@src")[-1]
        if poster:
            return {
                "name": self.__id__ + os.path.splitext(poster)[-1],
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
                    "name": "%s_%s.%s" % (self.__id__, index, type),
                    "url": url
                })

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
                result.append(
                    {
                        "url": build_torrent_url(url),
                        "link": url,
                        "name": self.__id__ + '_' + str(index) + '_' + size + '.torrent'
                    })

        return result

