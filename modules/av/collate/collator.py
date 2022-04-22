import os
import shutil
import concurrent.futures

from pathlib import Path
from enum import IntEnum

from modules.av import dictionary
from modules.av.collate.resolver import Resolver
from modules.av.collate.marauder.javdb import MarauderJavdb


class FileType(IntEnum):
    DIR = 1,
    FILE = 2


class Collator(object):
    def __init__(self, path, file_type=FileType.FILE):
        self.__paths__ = []

        if file_type == FileType.FILE:
            self.__append_files__(path)
        else:
            self.__append_dirfiles__(path)

        self.marauder = MarauderJavdb(True)

    def __append_files__(self, file_paths):
        if isinstance(file_paths, str):
            self.__paths__.append(file_paths)
        else:
            self.__paths__.extend(file_paths)

    def __append_dirfiles__(self, dir_path):
        for file in os.listdir(dir_path):
            self.__paths__.append(dir_path + "/" + file)

    def __neaten__(self, path):
        print("开始处理：" + path)

        try:
            info = None
            is_file = os.path.isfile(path)

            # 解析文件信息
            file_info = Resolver(self.marauder)
            file_info.resolve(path)

            if not is_file:
                # 重命名文件夹
                os.rename(path, file_info.dir)
            else:
                if not os.path.exists(file_info.dir):
                    # 创建文件夹
                    Path(file_info.dir).mkdir(exist_ok=True)

                new_path = file_info.dir + "/" + file_info.uid + '.' + file_info.type
                if path != new_path:
                    # 移动文件
                    shutil.move(path, file_info.dir + "/" + file_info.uid + '.' + file_info.type)

            # 下载封面
            if not os.path.exists(file_info.picture["path"]):
                self.__save_picture__(file_info.picture["content"], file_info.picture["path"])
                print("完成封面下载")

            # 下载剧照
            if file_info.stage_photos is not None and len(file_info.stage_photos) > 0:
                for stage_photo in file_info.stage_photos:
                    self.__save_picture__(stage_photo["content"], stage_photo["path"])
                print("完成剧照下载")

            excluded_types = ['torrent', 'jpg', 'png', 'gif']
            if file_info.type is not None and file_info.type not in excluded_types:
                dictionary.add(file_info.uid, file_info.dir)

        except Exception as error:
            print("处理出错:")
            print(error)
            os.system("pause")

        print("处理完成 " + path)

    def __save_picture__(self, picture_content, picture_path):
        with open(picture_path, "ab") as image:
            image.write(picture_content)

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as threadExecutor:
            threadExecutor.map(lambda path: self.__neaten__(path), self.__paths__)

        print('全部完成')
