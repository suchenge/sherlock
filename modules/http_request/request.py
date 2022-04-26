import requests
from urllib.parse import urlparse


def header(base_url):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5',
        'Connection': 'keep-alive',
        'Referer': base_url,
        'Cookie': 'theme=auto; over18=1; _ym_d=1633615771; _ym_uid=163361577147146056; locale=zh; _ym_isad=1; _jdb_session=VdlRFeDJ6IGRWPP5OGxl3WiG7P70eD%2F3QhpReNsbIE5LTrLhft7w5Y%2BCyH9CKWwTX9DlNWmOApPTMi1VIo3pe%2FjuDn7gMUv%2FnhogVY8%2BDeF0MhL%2Fpsy%2FYKu%2BKG7xUenbzqy1T8Hb2gcG6XCS0HElLCYSLj9NCp1BR%2FekXAauZaaI301uyrgEacbZSXYbQw74mGA%2BnIuRTw%2FBGVWDoyKlEmCmW9usIDGlv89eeHt15d6Bb1fAh1x4sfbxsajLpReIDo26M83dOJzrFb8aWJvdVpq7l5rIREAON9bS8M9a3xa1uG93q4EXhky0BT1nKz3xlTNDXa%2Fsj6G%2BY3yiBsJ24rU0IG3J1qTM6HMqKfHQbOglIZWH4Uh8hgyV%2Bttj%2FJ6%2BYrQ%3D--Ikf31DPn7D2a%2FEpY--4CJw51wWzsDPndUqqLKTRA%3D%3D'
    }


def monitoring(fun):
    def wrapper(*args, **kwargs):
        url = args[1]
        print("获取页面内容：" + url)
        result = fun(*args, **kwargs)
        return result

    return wrapper


class Request(object):
    def __init__(self, proxies=None):
        self.__proxies__ = proxies

    def __get_response__(self, url, headers):
        proxy = None

        if self.__proxies__:
            proxy = self.__proxies__.get()

            if proxy is None:
                raise Exception("没有获取到页面内容")

        try:
            response = requests.get(url, headers, proxies=proxy.address)
            if response and response.status_code == 200:
                if proxy:
                    proxy.rate += 1
                return response
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
