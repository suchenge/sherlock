import os
import re
import requests

from lxml import etree


class BaseMarauder(object):
    def __init__(self, open_proxy=False):
        self.open_proxy = open_proxy
        self.baseUrl, self.proxy = None, None

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5',
            'Connection': 'keep-alive',
            'Referer': self.baseUrl,
            'Cookie': 'theme=auto; over18=1; _ym_d=1633615771; _ym_uid=163361577147146056; locale=zh; _ym_isad=1; _jdb_session=VdlRFeDJ6IGRWPP5OGxl3WiG7P70eD%2F3QhpReNsbIE5LTrLhft7w5Y%2BCyH9CKWwTX9DlNWmOApPTMi1VIo3pe%2FjuDn7gMUv%2FnhogVY8%2BDeF0MhL%2Fpsy%2FYKu%2BKG7xUenbzqy1T8Hb2gcG6XCS0HElLCYSLj9NCp1BR%2FekXAauZaaI301uyrgEacbZSXYbQw74mGA%2BnIuRTw%2FBGVWDoyKlEmCmW9usIDGlv89eeHt15d6Bb1fAh1x4sfbxsajLpReIDo26M83dOJzrFb8aWJvdVpq7l5rIREAON9bS8M9a3xa1uG93q4EXhky0BT1nKz3xlTNDXa%2Fsj6G%2BY3yiBsJ24rU0IG3J1qTM6HMqKfHQbOglIZWH4Uh8hgyV%2Bttj%2FJ6%2BYrQ%3D--Ikf31DPn7D2a%2FEpY--4CJw51wWzsDPndUqqLKTRA%3D%3D'
        }

        proxy_address = "suchenge:suyuan2UnionPay@S1.go2https.com"
        self.proxy = {
            "http": "http://" + proxy_address
            , "https": "https://" + proxy_address
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
            raise Exception('get url content error, response status code:' + str(response.status_code))

    def __get_stage_photo__(self, stage_photos_url):
        print("获取剧照内容")
        stage_photos = []

        if stage_photos_url is not None and len(stage_photos_url) > 0:
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

