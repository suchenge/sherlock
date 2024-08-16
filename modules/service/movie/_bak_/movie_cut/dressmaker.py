import os

from modules.tools.http_request.request import Request
from modules.tools.http_request.proxy import Proxies
from modules.service.movie_cut.material import Material
from modules.service.movie_cut.material_folder import MaterialFolder


class Dressmaker(object):
    def __init__(self, path):
        self.__material__ = None
        self.__materials_folder__ = None
        self.__proxies__ = Proxies(**{})
        self.__request__ = Request(self.__proxies__)

        if os.path.isdir(path):
            self.__materials_folder__ = MaterialFolder(path)
        else:
            self.__materials__ = Material(path)

