from modules.tools.common_methods.unity_tools import parse_url


class Base(object):
    def __init__(self, url, html):
        self.__url__ = url
        self.__html__ = html
        self.__domain_url__, self.__url_path__ = parse_url(url)

    @staticmethod
    def is_match(url, html):
        return False

    def get_title(self):
        return None

    def get_child_page_url(self):
        return []

    def get_images(self, html, page_index=None):
        return []
