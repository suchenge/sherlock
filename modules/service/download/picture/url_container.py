class UrlContainer(object):
    def __init__(self, file_path, deduplication=False):
        self.__file_path__ = file_path
        self.__item__ = []

        with open(file_path, 'r', encoding='utf') as file:
            self.__items__ = file.readlines()

        if deduplication:
            self.__deduplication__()

    def items(self):
        return [item.replace('\n', '') for item in self.__items__]

    def __deduplication__(self):
        result = []

        for item in self.__items__:
            if item not in result:
                result.append(item)

        self.__items__ = result
        self.write()

    def write(self):
        with open(self.__file_path__, 'w', encoding='utf') as file:
            file.writelines(self.__items__)

    def append(self, url, auto_write=False):
        self.__items__.append(f'{url}\n')

        if auto_write:
            self.write()

    def is_exists(self, url):
        return f'{url}\n' in self.__items__

    def remove(self, url, auto_write=False):
        item_url = f'{url}\n'

        if item_url in self.__items__:
            self.__items__.remove(f'{url}\n')

        if auto_write:
            self.write()
