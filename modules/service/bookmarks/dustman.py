import re
import os.path

from modules.tools.http_request.http_client import HttpClient
from modules.tools.http_request.proxy import Proxies
from modules.tools.thread_pools.task_pool import TaskPool

from modules.service.bookmarks.bookmark import Bookmark
from modules.service.bookmarks.bookmark_group import BookmarkGroup, BookmarkGroups


def __get_bookmark_info__(bookmark_html_line):
    href, title, key = None, None, None
    match = re.compile(r'<A HREF="(.*?)" .*>(.*?)</A>').findall(bookmark_html_line)
    if match:
        href = match[0][0]
        title = match[0][1].replace('[FHDwmf]', '').replace('[HD]', '').replace('[FHD]', '').replace('【新提醒】', '')

        if title and ('javdb.com/v/' in href
                      or 'javhoo.org/ja/av/' in href
                      or 'youivr.com/youiv-' in href):
            key = title.split(' ')[0]

        if 'mgstage.com/product/' in href:
            href_paths = [path for path in href.split('/') if len(path) > 0]
            key = href_paths[len(href_paths) - 1]

        if 'www.ivworld.net/?p=' in href and title:
            title_match = re.compile(r'.*?\[(.*?)\].*?').findall(title)
            if title_match:
                key = title_match[0]

        if 'watchjavidol.com' in href and title and 'category' not in href:
            temp_href = href.replace('https://', '').replace('http://', '').split('/')
            if len(temp_href) > 2:
                key = title.split(' ')[0]

        if 'maddawgjav.net' in href and title:
            temp_href = href.replace('https://', '').replace('http://', '').split('/')
            if len(temp_href) > 2:
                temp_title = title.replace('[FHDwmf]', '').replace('[HD]', '').replace('[FHD]', '')
                key = temp_title.split(' ')[0]

        if key:
            key = key.upper()

            return {
                "href": href,
                "title": title,
                "key": key
            }
    else:
        return None


class Dustman(object):
    def __init__(self, bookmarks_html_file_path, bookmark_save_folder=None):
        self.__bookmarks_html_file_path__ = bookmarks_html_file_path
        self.__bookmarks_json_file_folder__ = os.path.dirname(bookmarks_html_file_path)

        if bookmark_save_folder is not None:
            self.__bookmarks_json_file_folder__ = bookmark_save_folder

        self.__bookmarks_groups__ = BookmarkGroups(self.__bookmarks_json_file_folder__)

    def save(self, group_line_qty=500):
        bookmarks = self.__get_bookmarks__()
        bookmarks_group = [bookmarks[i: i + group_line_qty] for i in range(0, len(bookmarks), group_line_qty)]

        index = 0

        for bookmarks_group_items in bookmarks_group:
            index = index + 1
            bookmark_group = BookmarkGroup(os.path.join(self.__bookmarks_json_file_folder__, "group_%s" % str(index).zfill(5)))
            bookmark_group.items = bookmarks_group_items
            bookmark_group.save()

            self.__bookmarks_groups__.append_group_path(bookmark_group.file_path)

        self.__bookmarks_groups__.save()

    def download(self):
        TaskPool.set_count(10)
        HttpClient.set_proxies(Proxies())

        for bookmark_group in self.__bookmarks_groups__.get_items():
            bookmark_group.download()

        TaskPool.join()
        
    def __get_bookmarks__(self):
        content = []
        line_index = 0
        with open(self.__bookmarks_html_file_path__, encoding='utf-8', mode='r') as html_file:
            while True:
                line = html_file.readline()
                if not line:
                    break

                if 'HREF' in line:
                    item = __get_bookmark_info__(line)
                    if item is not None:
                        line_index = line_index + 1

                        item["index"] = line_index
                        item["status"] = "open"
                        content.append(Bookmark(item))

        return content

