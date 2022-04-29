from lxml import etree
from modules.av.collate.marauder.base import BaseMarauder


class MarauderJavdb(BaseMarauder):
    def __init__(self, file, request):
        super().__init__(file, request)

        self.__base_url__ = "https://javdb34.com"
        search_url = self.__base_url__ + '/search?q=' + file.title + '&f=all'
        html_content = self.__get_url_content__(search_url)

        if html_content is None:
            raise Exception("没有获取到页面内容")

        tree = etree.HTML(html_content)

        links = tree.xpath("//div[@class='item']/a/@href")
        uids = tree.xpath("//div[@class='video-title']/strong/text()")

        if 0 < len(links) == len(uids) > 0:
            index = 0

            if file.title in uids:
                index = uids.index(file.title)
            else:
                for i in range(len(uids)):
                    if uids[i] in file.title:
                        index = i
                        break

            if index > -1:
                link = links[index]
                self.__content__ = self.__get_url_content__(self.__base_url__ + link)
                tree = etree.HTML(self.__content__)

                self.__id__ = uids[index]
                self.__title__ = tree.xpath("//h2[@class='title is-4']/strong/text()")[-1]
                self.__poster__ = tree.xpath("//img[@class='video-cover']/@src")[-1]
                self.__stills__ = tree.xpath("//div[@class='tile-images preview-images']/a[@class='tile-item']/@href")
        else:
            self.__content__ = None




