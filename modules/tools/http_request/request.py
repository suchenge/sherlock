import os
import requests

from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

from modules.tools.http_request.proxy import Proxies


def __mistiming_time__(start_time, end_time):
    seconds = (end_time - start_time).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


def header(base_url):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5',
        'Connection': 'keep-alive',
        'Referer': base_url,
        'Cookie': 'locale=zh; path=/; expires=Thu, 24 Jun 2027 10:54:57 GMT; SameSite=Lax;_jdb_session=qEIOkqLiro+wLxE8nnC1PHm9a9Y7dDcL2UQFPfOm5Blufq3JC8xLZL9h4W0pjzUJfMWLpNoVYjUBp831fhZPq+QDa7JLMxeLiKIpUM7oXid84ZWuj17GmdVC78Js5IOeDo8MPoOfBK9h07bhOiJK2tjg5t+ObflPYm0wnbeb5nBOsiXczMfozhvnLfrmhxaYuVhOqGUCzEZ5BkNUAly3k9K7sCrDXZf5hHL47nNg1LfKY9jHHypUgaa0s7AtQDZE/FQhOMb4nhXLpIQf92/JXg4n7+7MEheHTxvQPn3CTpNJLI6XXRoaqr9B+euXeSPgHfytv1M5s+a1OhD038IRBM+7I6xagj/7vLuXi53YiKCEu06EEaA0YleWnwVpwQ6MFcs=--4UMlp4y7NikHbzbx--XVysO9JH6l+uzpQjI0BS0A==; path=/; expires=Sat, 09 Jul 2022 10:54:57 GMT; secure; HttpOnly; SameSite=None'
    }


def monitoring(fun):
    def wrapper(*args, **kwargs):
        if len(args) > 1:
            url = args[1]
        else:
            url = args[0]
        # print("开始获取页面内容:%s" % url)
        task_start_time = datetime.now()
        result = fun(*args, **kwargs)

        descript = ""
        if result is None:
            descript = "无法"

        task_end_time = datetime.now()

        print("%s获取到请求内容[%s]:%s" % (descript, __mistiming_time__(task_start_time, task_end_time), url))

        return result

    return wrapper


class Request(object):
    def __init__(self, proxies: Proxies = None, circulation_proxy: bool = False):
        self.__proxies__ = proxies
        self.__circulation_proxy__ = circulation_proxy

    def __get_response__(self, url, headers, verify=False):
        proxy = None

        if self.__proxies__:
            proxy = self.__proxies__.get(self.__circulation_proxy__)

            if proxy is None:
                proxy = self.__proxies__.items[0]
                raise Exception("没有可用的Proxy，无法获取页面内容")

        try:
            response = None
            if proxy:
                response = requests.get(url, headers, proxies=proxy.address, verify=verify, timeout=60)
            else:
                response = requests.get(url, headers, verify=verify, timeout=60)

            if response and response.status_code == 200:
                if proxy:
                    proxy.rate += 1
                return response
            elif response.status_code == 404:
                return None
            else:
                if proxy:
                    proxy.available = False
                    return self.__get_response__(url, headers)
        except Exception as error:
            if proxy:
                proxy.available = False
                return self.__get_response__(url, headers)

    @monitoring
    def get(self, url):
        url_parse = urlparse(url)
        base_url = '%s://%s/' % (url_parse.scheme, url_parse.hostname)
        headers = header(base_url)
        response = self.__get_response__(url, headers)

        return response

    def get_text(self, url: str, encoding='utf-8'):
        response = self.get(url)
        if response:
            response.encoding = encoding
            return response.text
        else:
            return None

    def get_content(self, url: str, encoding='utf-8'):
        response = self.get(url)
        if response:
            response.encoding = encoding
            return response.content
        else:
            return None

    def download(self, **kwargs):
        path = kwargs["path"]
        url = kwargs["url"]

        if path and url:
            folder = os.path.dirname(path)

            if not os.path.exists(folder):
                Path(folder).mkdir(exist_ok=True)

        content = self.get_content(url)

        if content:
            with open(path, "ab") as file:
                file.write(content)
