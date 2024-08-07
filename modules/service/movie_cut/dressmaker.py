import os

from modules.tools.http_request.request import Request
from modules.tools.http_request.proxy import Proxies
from modules.service.movie_cut.materials import Materials


class Dressmaker(object):
    def __init__(self, path):
        self.__materials__ = []
        self.__proxies__ = Proxies(**{})
        self.__request__ = Request(self.__proxies__)

        if os.path.isdir(path):
            self.__materials__ = [Materials(os.path.join(path, file_name)) for file_name in os.listdir(path)]
        else:
            self.__materials__.append(Materials(path))

