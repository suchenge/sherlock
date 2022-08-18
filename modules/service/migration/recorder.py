import os
import xml.etree.ElementTree as etree

from modules.service.migration.worker import Worker


class Recorder(Worker):
    def __init__(self, directory):
        super(Recorder, self).__init__(directory)

    def append(self, source_path, target_path, is_file):
        tags = source_path.split('\\')
        tags = tags[1:]

        current_element = self.__document__.getroot()

        counter = 0
        for tag in tags:
            xpath = 'path[@name="' + tag + '"]'
            element = current_element.find(xpath)
            attribute = 'path'

            if element is None:
                if is_file:
                    attribute = 'file'

                current_element = etree.SubElement(current_element, attribute, {'name': tag})

                if is_file and counter == len(tags) - 1:
                    source_size = os.stat(source_path).st_size
                    current_element.set('completeness', '{:.2%}'.format(0))
                    etree.SubElement(current_element, 'source_path', {'size': str(source_size)}).text = source_path
                    etree.SubElement(current_element, 'target_path', {'size': '0'}).text = target_path
            else:
                current_element = element

            counter = counter + 1
