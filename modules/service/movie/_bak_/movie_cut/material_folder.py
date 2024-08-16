import os

from modules.tools.http_request.request import Request

from modules.service.movie_cut.material import Material


class MaterialFolder(object):
    def __init__(self, path):
        self.__materials__ = [Material(os.path.join(path, file_name)) for file_name in os.listdir(path)]
        self.__materials__ = [item for item in self.__materials__ if item.is_usable]

    def pigeonholed(self, request: Request):
        pass

    def clip(self):
        for material in self.__materials__:
            material.clip()

    def merge(self):
        pass
