import os
import re


class Resolver(object):
    def __init__(self, marauder):
        self.dir, self.uid, self.title, self.file_name = None, None, None, None
        self.picture, self.stage_photos = None, []

        self.__marauder__ = marauder

    def __match_file_name__(self, name):
        return re.match("^[a-z0-9A-Z-_]+$", name) is not None

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
        self.uid, self.title, self.picture, self.stage_photos = self.__marauder__.maraud(path_info)
        if self.uid is None or self.title is None or self.picture is None:
            print("文件解析失败")
            return

        print("获取文件信息：")
        print("uid：" + self.uid)
        print("title：" + self.title)
        print("picture：" + self.picture["url"])

        self.dir = dir + "/" + self.title

        self.picture["path"] = self.dir + "/" + self.picture["name"]

        for stage_photo in self.stage_photos:
            stage_photo["path"] = self.dir + "/" + stage_photo["name"]
