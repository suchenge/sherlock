from lxml import etree

from modules.service.movie_warehouse.collate.file import VirtualFile
from modules.service.movie_warehouse.collate.marauder.base import BaseMarauder, find_configuration_node, build_torrent_url

from modules.framework.configuration_manager.configuration_setting import configuration_setting


@configuration_setting('../../config/movie-website.json', False, 'url',
                       lambda json: find_configuration_node(json, 'default'))
class MarauderJavdb(BaseMarauder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if isinstance(self.__file__, VirtualFile) and self.__file__.need_search is False:
            self.__build__(self.__file__.url, self.__file__.title)
        else:
            self.__base_url__ = kwargs["url"]

            search_url = self.__base_url__ + 'search?q=' + self.__file__.title + '&f=all' 
            html_content = self.__get_url_content__(search_url)

            if html_content is None:
                raise Exception("没有获取到页面内容:" + search_url)

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
                    self.__build__(self.__base_url__ + link, uids[index])
            else:
                self.__content__ = None

    def __build__(self, link, id):
        self.__content__ = self.__get_url_content__(link)
        self.__url__ = link

        if self.__content__ is None:
            raise Exception("没有获取到页面内容:" + link)

        parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.HTML(self.__content__, parser)

        self.__id__ = id

        title_element = tree.xpath("//span[@class='origin-title']/text()")
        if title_element is None or len(title_element) == 0:
            title_element = tree.xpath("//strong[@class='current-title']/text()")

        self.__title__ = title_element[-1]

        self.__title__ = self.__id__ + " " + self.__title__

        self.__poster__ = tree.xpath("//img[@class='video-cover']/@src")[-1]
        self.__stills__ = tree.xpath("//div[@class='tile-images preview-images']/a[@class='tile-item']/@href")
        magent_links = tree.xpath("//div[@id='magnets-content']")[-1]

        if magent_links is not None and len(magent_links) > 0:
            index = 0
            for link in magent_links:
                index = index + 1
                info = link.getchildren()[0].find("a")
                url = info.get("href")
                size = info.getchildren()[2].text.strip()
                self.__torrents__.append({
                    "url": build_torrent_url(url),
                    "link": url,
                    "name": self.__id__ + '_' + str(index) + '_' + size + '.torrent'
                })

