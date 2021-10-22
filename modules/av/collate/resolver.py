import os
import re

from modules.av.collate.parse import parser


class Resolver(object):
    def __init__(self, get_function):
        self.dir, self.uid, self.title, self.file_name = None, None, None, None
        self.picture, self.stage_photos = None, []

        self.__get_function = get_function

    def __match_file_name__(self, name):
        return re.match("^[a-z0-9A-Z-_]+$", name) is not None

    def __get_stage_photo__(self, stage_photos_url):
        print("获取剧照内容")
        if stage_photos_url is not None and len(stage_photos_url) > 0:
            for stage_photo_url in stage_photos_url:
                print(stage_photo_url)
                stage_photo_name = os.path.split(stage_photo_url)[-1]
                self.stage_photos.append({
                    "name": stage_photo_name,
                    "url": stage_photo_url,
                    "path": self.dir + "/" + stage_photo_name,
                    "content": parser.get_url_content(stage_photo_url)
                })

    def __get_picture__(self, picture_url):
        print("获取封面内容")
        print(picture_url)
        picture_name = self.uid + os.path.splitext(picture_url)[-1]
        self.picture = {
            "name": picture_name,
            "url": picture_url,
            "path": self.dir + "/" + picture_name,
            "content": parser.get_url_content(picture_url)
        }

    def resolve(self, path):
        path_info = None

        dir, file = os.path.split(path)
        path_info = file
        self.file_name = file

        if os.path.isfile(path):
            path_info, file_suffix = os.path.splitext(file)
            self.file_name = file

        if not self.__match_file_name__(path_info):
            print("文件名称不符合规范")
            return

        # 获取文件信息
        self.uid, self.title, picture_url, stage_photos_url = self.__get_function(path_info)
        if self.uid is None or self.title is None or picture_url is None:
            print("文件解析失败")
            return

        print("获取文件信息：")
        print("uid：" + self.uid)
        print("title：" + self.title)
        print("picture：" + picture_url)

        self.dir = dir + "/" + self.title

        # 获取图片内容
        self.__get_picture__(picture_url)

        # 获取剧照内容
        self.__get_stage_photo__(stage_photos_url)
