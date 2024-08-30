import os
import platform

from urllib.parse import urlparse

def is_mac_os():
    return platform.system() == 'Darwin'

def parse_url(url):
    url_info = urlparse(url)
    return url_info.scheme + "://" + url_info.netloc, url_info.path

def get_file_suffix(url):
    name = os.path.split(url)[-1]
    suffix = name.split(".")[-1]
    if suffix == 'webp':
        suffix = 'jpg'
    return suffix

def format_title(title):
    if title is None:
        return None

    title = title.replace('\'', '')
    title = title.replace('/', '')
    title = title.replace('"', '')
    title = title.replace(':', '')
    title = title.replace('?', '')
    title = title.replace('*', '')
    title = title.replace('"', '')
    title = title.replace('<', '')
    title = title.replace('>', '')

    return title.strip()[0:150]

def ffmpeg_execute_path():
    if is_mac_os() is False:
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ffmpeg.exe')
    else:
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ffmpeg')

def is_file(path):
    types = ['mkv', 'MKV', 'mp4', 'MP4', 'avi', 'AVI', 'wmv', 'WMV']

    for file_type in types:
        if path.endswith(f'.{file_type}'):
            return True

    return False


