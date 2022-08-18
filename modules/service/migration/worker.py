import os
import shutil
import time
import threading
import xml.dom.minidom as xml
import xml.etree.ElementTree as etree


class Worker(object):
    def __init__(self, directory):
        self.__stop_thread__ = True
        self.__sleep_time__ = 5

        self.__root_name__ = 'record'
        self.__path__ = os.path.join(directory, 'migration record.xml')

        if not os.path.exists(self.__path__):
            root = etree.Element(self.__root_name__)
            self.__document__ = etree.ElementTree(root)
        else:
            self.__document__ = etree.parse(self.__path__)
            shutil.copyfile(self.__path__, self.__path__ + '.' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.bak')

    def start(self):
        self.__stop_thread__ = False
        threading.Thread(target=self.__thread_write__).start()

    def stop(self):
        self.__stop_thread__ = True

        time.sleep(self.__sleep_time__)

        self.__write_xml__()

    def __thread_write__(self):
        while not self.__stop_thread__:
            self.__write_xml__()
            time.sleep(self.__sleep_time__)

    def __write_xml__(self):
        try:
            xml_content = etree.tostring(self.__document__.getroot(), encoding='unicode')
            xml_content = xml_content.replace('\n', '').replace('\t', '')

            document = xml.parseString(xml_content)

            with open(self.__path__, 'w', encoding='utf-8') as file:
                document.writexml(file, indent='', addindent='\t', newl='\n', encoding='UTF-8')
                file.close()
        except Exception as error:
            print(error)
