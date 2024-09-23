from modules.tools.common_methods.unity_tools import parse_url, format_title

from modules.service.download.picture.strategy.provider import ResolverStrategyProvider


class Resolver(object):
    def __init__(self, url):
        self.__url__ = url

        self.__domain_url__, self.__url_path__ = parse_url(url)
        self.__strategy__ = ResolverStrategyProvider.get_strategy(self.__url__)

    def get_title(self):
        title = self.__strategy__.get_title()
        return format_title(title)

    def get_images(self):
        return self.__strategy__.__get_images__()

    def download_image(self, **images):
        return self.__strategy__.download_image(**images)
