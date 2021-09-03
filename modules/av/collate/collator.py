import os
import re
import shutil
import concurrent.futures

from pathlib import Path
from enum import IntEnum

from modules.av import dictionary
from modules.av.collate.parse import parser


class FileType(IntEnum):
    DIR = 1,
    FILE = 2


class Collator(object):
    def __init__(self, path, file_type=FileType.FILE):
        self.__paths = []

        if file_type == FileType.FILE:
            self.__append_files(path)
        else:
            self.__append_dirfiles(path)


    def __append_files(self, file_paths):
        if isinstance(file_paths, str):
            self.__paths.append(file_paths)
        else:
            self.__paths.extend(file_paths)


    def __append_dirfiles(self, dir_path):
        for file in os.listdir(dir_path):
            self.__paths.append(dir_path + "/" + file)


    def __neaten(self, path):
        info = None
        if os.path.isfile(path):
            info = self.__file_neaten(path)
        else:
            info = self.__dir_neaten(path)

        dictionary.add(info["uid"], info["dir"])

        print("done " + path)

    def __dir_neaten(self, dirpath):
        dir, file = os.path.split(dirpath)

        if not self.__match_file_name(file):
            return

        # 获取文件信息
        uid, title, picture = parser.get_info_1(file)

        if uid and title and picture:
            new_dir = dir + "/" + title
            new_picturename = uid + os.path.splitext(picture)[-1]
            new_picturepath = new_dir + "/" + new_picturename

            # 重命名文件夹
            os.rename(dirpath, new_dir)
            # 下载图片
            if not os.path.exists(new_picturepath):
                self.__download_picture(picture, new_picturepath)

        return {"uid": uid, "dir": new_dir}


    def __file_neaten(self, filepath):
        dir, file = os.path.split(filepath)
        filename, filesuffix = os.path.splitext(file)

        if not self.__match_file_name(filename):
            return

        # 获取文件信息
        uid, title, picture = parser.get_info_1(filename)

        if uid and title and picture:
            new_dir = dir + "/" + title
            new_filename = uid + filesuffix
            new_picturename = uid + os.path.splitext(picture)[-1]
            new_filepath = new_dir + "/" + new_filename
            new_picturepath = new_dir + "/" + new_picturename

            # 创建文件夹
            Path(new_dir).mkdir(exist_ok=True)
            # 移动文件
            shutil.move(filepath, new_filepath)
            # 下载图片
            if not os.path.exists(new_picturepath):
                self.__download_picture(picture, new_picturepath)

        return {"uid": uid, "dir": new_dir}


    def __match_file_name(self, name):
        return re.match("^[a-z0-9A-Z-]+$", name) is not None

    def __download_picture(self, picture_url, picture_path):
        with open(picture_path, "ab") as image:
            image.write(parser.get_url_content(picture_url))

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as threadExecutor:
            threadExecutor.map(lambda path: self.__neaten(path), self.__paths)


