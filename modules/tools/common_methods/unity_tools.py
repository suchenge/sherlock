import os
import platform

from urllib.parse import urlparse

class UnityTools(object):
    def __int__(self):
        pass

    @staticmethod
    def is_mac_os():
        return platform.system() == 'Darwin'

    @staticmethod
    def parse_url(url):
        url_info = urlparse(url)
        return url_info.scheme + "://" + url_info.netloc, url_info.path

    @staticmethod
    def get_file_suffix(url):
        name = os.path.split(url)[-1]
        suffix = name.split(".")[-1]

        if suffix == 'webp':
            suffix = 'jpg'

        return suffix

    @staticmethod
    def ffmpeg_execute_path():
        if UnityTools.is_mac_os() is False:
            return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ffmpeg.exe')
        else:
            return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ffmpeg')
