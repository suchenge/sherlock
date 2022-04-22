import os
import re

from concurrent.futures import ThreadPoolExecutor, as_completed
from modules.http_request.request import Request


class BaseMarauder(object):
    def __init__(self, open_proxy=False):
        self.open_proxy = open_proxy
        self.http_request = Request()

    def __format_title__(self, title):
        return re.compile("[?:*'<>/\\\]").sub("", title).strip()

    def __get_url_content__(self, url, is_html=True):
        response = self.http_request.get(url, self.open_proxy)

        if response.status_code == 200:
            if is_html:
                return response.text
            else:
                return response.content
        else:
            raise Exception('get url content error, response status code:' + str(response.status_code))

    def __get_stage_photo__(self, uid, stage_photos_url):
        print("获取剧照内容")
        stage_photos = []

        if stage_photos_url is not None and len(stage_photos_url) > 0:
            with ThreadPoolExecutor(max_workers=5) as executor:
                tasks = [executor.submit(self.__build_stage_photo__, uid, index, stage_photos_url) for index in range(0, len(stage_photos_url))]

                for future in as_completed(tasks):
                    result = future.result()
                    stage_photos.append(result)

        return stage_photos

    def __build_stage_photo__(self, uid, index, stage_photos_url):
        stage_photo_url = stage_photos_url[index]
        stage_photo_name = os.path.split(stage_photo_url)[-1]
        stage_photo_type = stage_photo_name.split('.')[-1]

        print('index = %d, stage_photo_url = %s' % (index, stage_photo_url))

        return {
            "name": '%s_%s.%s' % (uid, index, stage_photo_type),
            "url": stage_photo_url,
            "content": self.__get_url_content__(stage_photo_url, False),
        }

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

