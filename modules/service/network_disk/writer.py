import os

from selenium import webdriver

from modules.service.network_disk.link import Link

class Writer(object):
    def __init__(self):
        '''
        self.__browser__ = webdriver.Chrome()
        '''

    def write(self):
        link_folder = os.path.abspath("../data/pan_links")
        links = [Link(os.path.join(link_folder, file)) for file in os.listdir(link_folder)]

        for link in links:
            link.write(None)
