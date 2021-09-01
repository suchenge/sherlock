import xml.etree.ElementTree as ElementTree


class PageUrl(object):
    items = []

    def __init__(self, file_path):
        __urlXml = ElementTree.parse(file_path)
        __xmlRoot = __urlXml.getroot()

        for node in __xmlRoot:
            self.items.append(node.attrib["HREF"])
