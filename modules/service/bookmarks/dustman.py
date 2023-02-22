import os.path
import re

from modules.tools.http_request.request import Request
from modules.tools.http_request.proxy import Proxies
from modules.tools.thread_pools.task_pool import TaskPool

from modules.service.movie_warehouse.collate.file import VirtualFile
from modules.service.movie_warehouse.collate.marauder.javdb import MarauderJavdb

from modules.service.bookmarks.bookmark import Bookmark
from modules.service.bookmarks.bookmark_group import BookmarkGroup


class Dustman(object):
    def __init__(self, bookmarks_html_file_path):
        self.__bookmarks_html_file_path__ = bookmarks_html_file_path
        self.__bookmarks_json_file_folder = os.path.dirname(bookmarks_html_file_path)

    def save(self, group_line_qty=500):
        bookmarks = self.__get_bookmarks__(self.__bookmarks_html_file_path__)
        bookmarks_groups = [bookmarks[i: i + group_line_qty] for i in range(0, len(bookmarks), group_line_qty)]

        index = 0
        for bookmarks_group_items in bookmarks_groups:
            index = index + 1
            bookmark_group = BookmarkGroup(self.__bookmarks_json_file_folder, index)
            bookmark_group.items = bookmarks_group_items
            bookmark_group.inspection()

    def download(self, save_base_path):
        TaskPool.set_count(10)
        request = Request(Proxies(**{}))

        bookmark_groups = []

        for file_name in os.listdir(self.__bookmarks_json_file_folder):
            bookmark_group = BookmarkGroup.build(os.path.join(self.__bookmarks_json_file_folder, file_name))

            if bookmark_group is not None:
                bookmark_groups.append(bookmark_group)

        for bookmark_group in bookmark_groups:
            bookmark_group.download(lambda bookmark: self.__build_film__(bookmark, save_base_path, request), request)

    def __build_film__(self, bookmark, save_base_path, request):
        file = {
            "name": "",
            "title": bookmark["key"],
            "folder": os.path.join(save_base_path,bookmark["title"]),
            "path": save_base_path,
            "url": bookmark["href"]
        }

        marauder = MarauderJavdb(**{'file': VirtualFile(file), 'request': request})
        return marauder.to_film()

    def __get_bookmarks__(self, bookmarks_file_path):
        content = []
        line_index = 0
        with open(bookmarks_file_path, encoding='utf-8', mode='r') as html_file:
            while True:
                line = html_file.readline()
                if not line:
                    break

                if 'HREF' in line:
                    item = self.__get_bookmark_info__(line)
                    if item is not None:
                        line_index = line_index + 1

                        item["index"] = line_index
                        item["status"] = 'open'
                        content.append(Bookmark().build(item))

        return content

    def __get_bookmark_info__(self, bookmark):
        href, title, key = None, None, None
        match = re.compile(r'<A HREF="(.*?)" .*>(.*?)</A>').findall(bookmark)
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

