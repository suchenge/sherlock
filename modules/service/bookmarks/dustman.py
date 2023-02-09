import \
    os.path
import re
import json

from modules.tools.http_request.request import Request
from modules.tools.http_request.proxy import Proxies

from modules.service.movie_warehouse.collate.porter import Porter
from modules.service.movie_warehouse.collate.marauder.javdb import MarauderJavdb


class Dustman(object):
    def __init__(self, bookmarks_file_path, url_file_path):
        self.__url_file_path__ = url_file_path

        line_index = 1
        url_contents = []

        with open(bookmarks_file_path, encoding='utf-8', mode='r') as bookmarks:
            while True:
                line = bookmarks.readline()
                if not line:
                    break

                if 'HREF' in line:
                    bookmark = self.__get_bookmark_info__(line)
                    if bookmark is not None:
                        line_index = line_index + 1
                        bookmark["index"] = line_index
                        bookmark["status"] = 'open'
                        url_contents.append(bookmark)

        if url_contents and len(url_contents) > 0:
            with open(url_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(url_contents, json_file, indent=4, ensure_ascii=False)

    def clean_up(self, save_base_path):
        request = Request(Proxies(**{}))

        with open(self.__url_file_path__, 'r', encoding='utf-8') as json_file:
            bookmarks = json.load(json_file)

        for bookmark in bookmarks:
            try:
                file = {
                    "name": "",
                    "title": bookmark.key,
                    "folder": os.path.join(save_base_path, bookmark.title),
                    "path": os.path.dirname(save_base_path)
                }

                marauder = MarauderJavdb(**{'file': file, 'request': request})
                film = marauder.to_film()

                porter = Porter(film)
                porter.save_poster(request)
                porter.save_stills(request)
                porter.save_torrents(request)

                bookmark['status'] = 'done'
            except Exception as error:
                print(error)

        with open(self.__url_file_path__, 'w', encoding='utf-8') as json_file:
            json.dump(self.__url_file_path__, json_file, indent=4, ensure_ascii=False)

    def __get_bookmark_info__(self, bookmark):
        href, title, key = None, None, None
        match = re.compile(r'<A HREF="(.*?)" .*>(.*?)</A>').findall(bookmark)
        if match:
            href = match[0][0]
            title = match[0][1]

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

