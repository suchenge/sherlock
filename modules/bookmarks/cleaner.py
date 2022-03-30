import os
import re


class Cleaner(object):
    def __init__(self):
        self.__bookmarks_path__ = os.path.abspath("../data/bookmarks/bookmarks_2022_3_30.html")
        self.__bookmarks_context__ = []
        self.__bookmarks_groups__ = {}

        line_index = 0
        with open(self.__bookmarks_path__, encoding='utf-8', mode='r') as bookmarks:
            while True:
                line_index += 1
                line = bookmarks.readline()
                if not line:
                    break

                self.__bookmarks_context__.append({'line_index': line_index, 'context': line})

                if 'HREF' in line and self.__is_effective_line__(line):
                    match = re.compile(r'<A HREF=\"(http[s]?://(.*?)/.*?)\".*?>(.*?)</A>').findall(line)

                    if match:
                        href = match[0][0]
                        domain = match[0][1]
                        title = match[0][2]
                        keys = self.__get_key__(title, href)
                        overdue = self.__dictionary_is_exists__(keys)

                        for key in keys:
                            self.__append_to_groups__(self.__build_context__(line_index, line, href, domain, title, key, overdue))

    def run(self):
        print(self.__bookmarks_context__[len(self.__bookmarks_context__) - 1]['line_index'])
        print(len(self.__bookmarks_groups__.values()))

        for key, values in self.__bookmarks_groups__.items():
            self.__clear_bookmarks_context__(values)

            print(key)
            for value in values:
                print('key:%s | delete:%s | domain:%s  | line_index: %s| href:%s' % (value['key'], value['delete'], value['domain'], value['line_index'], value['href']))
            print('--------------------------------------------------------------')

    def __clear_bookmarks_context__(self, group):
        # 如果链接组有一个已经失效，那此链接组中所有链接都失效
        if True in self.__get_value_by_group__(group, 'delete'):
            for context in group:
                context['delete'] = True
        # 如果当前链接组中有重复的链接，则只保留一个链接

        # 如果链接组中含有‘javdb’的链接，则其他链接失效
        elif 'javdb.com' in self.__get_value_by_group__(group, 'domain'):
            for context in group:
                if 'javdb.com' not in context['domain']:
                    context['delete'] = True

    def __get_value_by_group__(self, group, key):
        result = []
        for value in group:
            result.append(value[key])

        return result

    def __append_to_groups__(self, context):
        key = context['key']
        if key in self.__bookmarks_groups__.keys():
            self.__bookmarks_groups__[key].append(context)
        else:
            self.__bookmarks_groups__[key] = [context]

    def __is_effective_line__(self, line):
        domains = ['141jav', 'javdb', 'javhoo', 'watchjavonline', 'sehuatang', 'taohuazu9', 'c700', 'sis001', 'javtorrent', 'maddawgjav', 'mgstage', 'jpvrporn', 'bejav', 'ivworld', 'watchjavidol', 'youivr', 'canchah2016', 'dmm']
        for domain in domains:
            if domain in line:
                return True

        return False

    def __build_context__(self, line_index, line, href, domain, title, key, delete):
        return {'line_index': line_index, 'href': href, 'domain': domain, 'title': title, 'key': key, 'delete': delete}

    def __get_key__(self, title, href):
        for r in ['[FHD]', '[FHDwmf]', '[HD]']:
            title = title.replace(r, '').replace(r.upper(), '').replace(r.lower(), '')

        match = re.compile(r'^([a-zA-Z0-9-]+).*?$').findall(title)
        if match:
            key = match[0]
        else:
            href_paths = [path for path in href.split('/') if len(path) > 0]
            key = href_paths[len(href_paths) - 1]

        match = re.compile(r'^(\d+)(.*?)$').findall(key)
        if not match:
            return [key]
        else:
            return [match[0][1], key]

    def __dictionary_is_exists__(self, keys):
        dictionary_base_path = 'D:\\Dictionary\\indexs\\%s.json'
        for key in keys:
            if os.path.exists(dictionary_base_path % key):
                return True

        return False


