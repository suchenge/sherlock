import os
import threading
import xml.etree.ElementTree as ElementTree

from queue import Queue


class PageUrl(object):
    def __init__(self, file_path):
        self.items = []
        self.__file_path = file_path
        self.__done_url_path = os.path.abspath("data/source/") + "/done.txt"
        self.__done_items = Queue()
        self.__urlXml = ElementTree.parse(file_path)
        self.__xmlRoot = self.__urlXml.getroot()

        self.__remove_repeated_node()

        for node in self.__xmlRoot:
            if node.attrib["HREF"] not in self.items:
                self.items.append(node.attrib["HREF"])

        self.__remove_done_url()

        threading.Thread(target=self.__write, daemon=True).start()

    # source数据去重
    def __remove_repeated_node(self):
        r_node = []
        for index in range(len(self.__xmlRoot)):
            current_node = self.__xmlRoot[index]
            for cindex in range(len(self.__xmlRoot)):
                other_node = self.__xmlRoot[cindex]
                if other_node.attrib["HREF"].replace("\n", "").replace("\r", "") == current_node.attrib["HREF"].replace("\n", "").replace("\r", "") and cindex != index:
                    r_node.append(other_node)

        if len(r_node) > 0:
            for node in r_node:
                if node in self.__xmlRoot:
                    self.__xmlRoot.remove(node)

            new_xml = ElementTree.ElementTree(self.__xmlRoot)
            new_xml.write(self.__file_path, encoding="utf-8")

    def __remove_done_node(self, url):
        done_nodes = self.__xmlRoot.findall("A[@HREF='" + url + "']")

        if len(done_nodes) > 0:
            for node in done_nodes:
                self.__xmlRoot.remove(node)

            new_xml = ElementTree.ElementTree(self.__xmlRoot)
            new_xml.write(self.__file_path, encoding="utf-8")

    def __remove_done_url(self):
        if os.path.exists(self.__done_url_path):
            find_remove_url = False
            with open(self.__done_url_path, "r", encoding='utf-8') as url:
                done_urls = url.readlines()

                for done_url in done_urls:
                    url = done_url.replace("\n", "").replace("\r", "")
                    if url in self.items:
                        find_remove_url = True
                        self.items.remove(url)
                        done_nodes = self.__xmlRoot.findall("A[@HREF='" + url + "']")

                        for node in done_nodes:
                            self.__xmlRoot.remove(node)

            if find_remove_url:
                new_xml = ElementTree.ElementTree(self.__xmlRoot)
                new_xml.write(self.__file_path, encoding="utf-8")

    def done(self, url, folder=None):
        message = "done " + url
        if folder:
            message += " folder: " + folder

        print(message)
        self.__done_items.put(url)

    def __write(self):
        while True:
            if self.__done_items.qsize() > 0:
                done_url = self.__done_items.get()

                with open(self.__done_url_path, 'a', encoding='utf-8') as log:
                    log.write(done_url + "\r")

                self.__remove_done_node(done_url)
