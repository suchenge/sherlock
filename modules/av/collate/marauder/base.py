import os
import re
import requests

from lxml import etree


class BaseMarauder(object):
    def __init__(self, open_proxy=False):
        self.open_proxy = open_proxy
        self.baseUrl, self.proxy = None, None

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Referer': self.baseUrl,
            'Cookie': 'theme=auto; over18=1; _ym_d=1633615771; _ym_uid=163361577147146056; locale=zh; remember_me_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkluQmxNV3A2YUhOSFRVZ3llWGRVWjI5eWJVTjRJZz09IiwiZXhwIjoiMjAyMS0xMC0yOVQwMzo1NDo1NS4wMDBaIiwicHVyIjoiY29va2llLnJlbWVtYmVyX21lX3Rva2VuIn19--a4fc9d154fd862fcafea2558c182187c8bb5b510; _ym_isad=1; _jdb_session=Lwhd0aqrITh18nGnY1Xim7XtRAlg%2Bxxy9KMALBWQAB2usUgnjcJpipZNkvNsECbaTd1UaG04AI6%2BOiFdf8AHd%2Fx79sxP425vEP1UC825U6mTwLlZdYd0gTdVrlymXlbjNoUstszaXZRXR%2BA6ep1Lubgpbg3Ht1eaYB1RpnuM%2FBoO3tLg1NCDcPmvrqcAW4uHvC%2BibE1YlBVHW3k63g7HRfjC8fkKrHrQMpdBB15RpDlEiZ2PaxLRtNeL59hUSAb62LChrnnIYW54eH7yRWjhaZwczXMAJdnU7ywbNPe2%2FYiuQJVhNMGvspj%2FweOPSraxfkvNDUwbzIRLDvQ7A55cEkrWyNo5bEa%2FmR0%2FGdah%2BWj8HDUt7IOh2AREMEH0RgfR9Sg%3D--pQrKHpNvmvw5waYR--%2BhRb3P9XrK4cC%2FLHUJkQvg%3D%3D'
        }

    def __format_title__(self, title):
        return re.compile("[?:*'<>/\\\]").sub("", title).strip()

    def __get_url_content__(self, url, is_html=True):
        if not self.open_proxy:
            self.proxy = None

        response = requests.get(url, headers=self.headers, proxies=self.proxy)
        if response.status_code == 200:
            if is_html:
                return response.text
            else:
                return response.content
        else:
            raise Exception('get url content error, response status code:' + response.status_code)

    def __get_stage_photo__(self, stage_photos_url):
        print("获取剧照内容")
        if stage_photos_url is not None and len(stage_photos_url) > 0:
            stage_photos = []
            for stage_photo_url in stage_photos_url:
                print(stage_photo_url)
                stage_photo_name = os.path.split(stage_photo_url)[-1]
                stage_photos.append({
                    "name": stage_photo_name,
                    "url": stage_photo_url,
                    "content": self.__get_url_content__(stage_photo_url, False)
                })

            return stage_photos

    def __get_picture__(self, uid, picture_url):
        print("获取封面内容")
        print(picture_url)
        picture_name = uid + os.path.splitext(picture_url)[-1]
        return {
            "name": picture_name,
            "url": picture_url,
            "content": self.__get_url_content__(picture_url, False)
        }

    def maraud(self, filename):
        pass

