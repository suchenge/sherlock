import json
import os
import time
import threading
import modules.http_request.json_path


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


def monitoring(fun):
    def wrapper(*args, **kwargs):
        obj = args[0]
        current_item = obj.__current_item__
        result = fun(*args, **kwargs)
        if current_item != result:
            print('当前Proxy：' + result.__proxyObj__['address'])

        return result

    return wrapper


@singleton
class Proxies(object):
    def __init__(self):
        self.__path__ = os.path.join(os.path.dirname(modules.http_request.json_path.__file__), 'proxies.json')

        with open(self.__path__, 'r') as json_file:
            self.__proxies__ = json.load(json_file)

        self.__items__ = [Proxy(proxy) for proxy in self.__proxies__]
        self.__current_item__ = None

        thread = threading.Thread(target=self.__write__)
        thread.setDaemon(True)
        thread.start()
        # threading.Thread(target=self.__write__).start()

    @monitoring
    def get(self):
        if self.__current_item__ is not None and self.__current_item__.available == True:
            return self.__current_item__

        available_items = sorted(
            [item for item in self.__items__ if item.available == True and item != self.__current_item__],
            key=lambda x: x.rate, reverse=True)

        if available_items and len(available_items) > 0:
            self.__current_item__ = available_items[0]
            return self.__current_item__
        else:
            return None

    def __write__(self):
        while True:
            try:
                with open(self.__path__, 'w') as json_file:
                    json.dump(self.__proxies__, json_file, indent=4)
            except Exception as error:
                print(error)
            time.sleep(10)


class Proxy(object):
    def __init__(self, proxyObj):
        self.__proxyObj__ = proxyObj
        self.__address__ = proxyObj['address']
        self.__rate__ = proxyObj['rate']
        self.__available__ = True

    @property
    def address(self):
        return {
            'http': 'http://%s@%s' % ('suchenge:suyuan2UnionPay', self.__address__)
            , 'https': 'https://%s@%s' % ('suchenge:suyuan2UnionPay', self.__address__)
        }

    @property
    def rate(self): return self.__rate__

    @rate.setter
    def rate(self, value):
        self.__rate__ = value
        self.__proxyObj__['rate'] = value

    @property
    def available(self): return self.__available__

    @available.setter
    def available(self, value):
        if value is False:
            self.__available__ = False
            self.rate -= 1
