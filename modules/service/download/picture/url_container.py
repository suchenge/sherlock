class UrlContainer(object):
    def __init__(self, file_path):
        self.__file_path__ = file_path
        self.__item__ = []

        with open(file_path, 'r', encoding='utf') as file:
            self.__items__ = file.readlines()

    def items(self):
        return [item.replace('\n', '') for item in self.__items__]

    def write(self):
        with open(self.__file_path__, 'a', encoding='utf') as file:
            file.writelines(self.__items__)

    def append(self, url, auto_write=False):
        self.__items__.append(f'{url}\n')

        if auto_write:
            self.write()

    def is_exists(self, url):
        return f'{url}\n' in self.__items__

    def remove(self, url, auto_write=False):
        self.__items__.remove(f'{url}\n')

        if auto_write:
            self.write()