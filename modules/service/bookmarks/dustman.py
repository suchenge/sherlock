import json
import re
import os.path

from modules.tools.http_request.http_client import HttpClient
from modules.tools.http_request.proxy import Proxies
from modules.tools.thread_pools.task_pool import TaskPool

from modules.service.bookmarks.bookmark import Bookmark


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
        self.__html_file_path__ = bookmarks_html_file_path
        self.__json_file_folder__ = os.path.dirname(bookmarks_html_file_path)

        self.__download_item_folder = os.path.join(self.__json_file_folder__, "downloading")
        self.__done_item_folder__ = os.path.join(self.__json_file_folder__, "done")

        self.__done_json_file_path__ = os.path.join(self.__json_file_folder__, "done.json")
        self.__error_json_file_path__ = os.path.join(self.__json_file_folder__, "error.json")
        self.__open_json_file_path__ = os.path.join(self.__json_file_folder__, "open.json")

        self.__open_items__ = None
        self.__error_items__ = None
        self.__done_items__ = None

    def save(self):
        items = self.__get_bookmarks__()
        with open(self.__open_json_file_path__, "w", encoding="utf-8") as file:
            json.dump(items, file, indent=4, ensure_ascii=False)

    def download(self):
        HttpClient.set_proxies(Proxies())
        items = self.open_items

        for item in items:
            bookmark = Bookmark(**item)
            item_path = item.get("path")

            try:
                if item_path and os.path.exists(item_path):
                    information = bookmark.get_information(item_path)
                    bookmark.inspection(information, item_path)
                else:
                    bookmark.download(item_path)
            except Exception as error:
                bookmark.status = "error"
            finally:
                self.save_all_items(items)

    @property
    def open_items(self):
        if self.__open_items__ is None:
            self.__open_items__ = self.__build_items__(self.__open_json_file_path__)
        return self.__open_items__

    @property
    def error_items(self):
        if self.__error_items__ is None:
            self.__error_items__ = self.__build_items__(self.__error_json_file_path__)
        return self.__error_items__

    @property
    def done_items(self):
        if self.__done_items__ is None:
            self.__done_items__ = self.__build_items__(self.__done_json_file_path__)
        return self.__done_items__

    def save_all_items(self, items):
        done_items = list(filter(lambda item: item.status == "done", items))
        error_items = list(filter(lambda item: item.status == "error", items))
        open_items = list(filter(lambda item: item.status == "open", items))

        self.__save_items_with_status__(done_items, self.__done_json_file_path__)
        self.__save_items_with_status__(error_items, self.__error_json_file_path__)
        self.__save_items_with_status__(open_items, self.__open_json_file_path__)

    def __save_items_with_status__(self, items, json_file_path):
        if items and len(items) > 0:
            with open(json_file_path, "w", encoding="utf-8") as file:
                json.dump([item.to_json() for item in items], file, ensure_ascii=False)

    def __build_items__(self, json_file_path):
        if os.path.exists(json_file_path):
            with open(json_file_path, "r", encoding="utf-8") as file:
                result = json.load(file)
                if result is not None and len(result) > 0:
                    return result
                else:
                    return []

    def __get_bookmarks__(self):
        content = []
        line_index = 0

        with open(self.__html_file_path__, encoding='utf-8', mode='r') as html_file:
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
                        content.append(item)

        return content

