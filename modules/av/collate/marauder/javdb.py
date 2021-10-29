import requests

from lxml import etree
from modules.av.collate.marauder.base import BaseMarauder


class MarauderJavdb(BaseMarauder):
    def __init__(self, open_proxy):
        super().__init__(open_proxy)
        self.baseUrl = "https://javdb33.com"

        proxy_address = "suchenge:suyuan2UnionPay@jp2.go2https.com"
        self.proxy = {
            "http": "http://" + proxy_address
            , "https": "https://" + proxy_address
        }

    def maraud(self, filename):
        url = self.baseUrl + '/search?q=' + filename + '&f=all'

        print("开始访问信息页面:")
        print("url：" + url)
        tree = etree.HTML(self.__get_url_content__(url))

        links = tree.xpath("//div[@class='grid-item column']/a/@href")
        uids = tree.xpath("//div[@class='grid-item column']/a/div[@class='uid']/text()")

        if 0 < len(links) == len(uids) > 0:
            index = 0

            if filename in uids:
                index = uids.index(filename)
            else:
                for i in range(len(uids)):
                    if uids[i] in filename:
                        index = i
                        break

            if index < 0:
                print("页面中没有查询到信息")
                return None, None, None, None

            uid = uids[index]

            if index > -1:
                link = links[index]
                print("url：" + self.baseUrl + link)
                tree = etree.HTML(self.__get_url_content__(self.baseUrl + link))

                title = tree.xpath("//h2[@class='title is-4']/strong/text()")[-1]
                picture = tree.xpath("//img[@class='video-cover']/@src")[-1]
                stage_photos = tree.xpath("//div[@class='tile-images preview-images']/a[@class='tile-item']/@href")

                if title and picture and uid:
                    uid = uid.upper().strip()
                    return uid, self.__format_title__(title), self.__get_picture__(uid, picture), self.__get_stage_photo__(stage_photos)
        else:
            print("页面中没有查询到信息")
