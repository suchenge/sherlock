import os
import json
from random import randint

from modules.framework.decorators.base_decorator import singleton
from modules.framework.configuration_manager.configuration_setting import configuration_setting


def monitoring(fun):
    def wrapper(*args, **kwargs):
        obj = args[0]
        current_item = obj.__current_item__

        result = fun(*args, **kwargs)

        if result is None:
            print('没有可用的Proxy')

        if current_item != result:
            print('当前Proxy：%s|%s' % (result.__proxy_obj__['address'], result.__proxy_obj__['rate']))

        return result

    return wrapper


def __setting_path__():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, '../../config/proxies.json')
    return path


@configuration_setting(__setting_path__(), True, 'setting')
@singleton
class Proxies(object):
    def __init__(self, **kwargs):
        authentication = kwargs['setting']['authentication']
        self.__proxies__ = kwargs['setting']['proxies']
        self.__config__ = {'authentication': authentication, 'proxies': self.__proxies__}

        self.__items__ = [Proxy(proxy, authentication) for proxy in self.__proxies__]
        self.__current_item__ = None

    @property
    def items(self):
        return self.__items__

    @monitoring
    def get(self, circulation_proxy: bool = False):
        if self.__current_item__ is not None and self.__current_item__.available is True:
            return self.__current_item__

        if circulation_proxy:
            items = [item for item in self.__items__ if item != self.__current_item__]

            item_index = randint(0, len(items) - 1)
            self.__current_item__ = items[item_index]
            return self.__current_item__
        else:
            available_items = sorted([item for item in self.__items__ if item.available is True and item != self.__current_item__],
                                     key=lambda x: x.rate,
                                     reverse=True)

            if available_items and len(available_items) > 0:
                self.__current_item__ = available_items[0]
                return self.__current_item__
            else:
                return None

    def close(self):
        self.__config__['proxies'] = sorted(self.__config__['proxies'], key=lambda x: x['rate'], reverse=True)

        with open(__setting_path__(), 'w') as json_file:
            json.dump(self.__config__, json_file, indent=4)


class Proxy(object):
    def __init__(self, proxy_object, authentication):
        self.__proxy_obj__ = proxy_object
        self.__address__ = proxy_object['address']
        self.__rate__ = proxy_object['rate']
        self.__available__ = True
        self.__authentication__ = authentication

    @property
    def address(self):
        return {
            'http': 'http://%s@%s' % (self.__authentication__, self.__address__)
            , 'https': 'https://%s@%s' % (self.__authentication__, self.__address__)
        }

    @property
    def proxy_address(self):
        return self.__address__

    @property
    def rate(self): return self.__rate__

    @rate.setter
    def rate(self, value):
        self.__rate__ = value
        self.__proxy_obj__['rate'] = value

    @property
    def available(self): return self.__available__

    @available.setter
    def available(self, value):
        if value is False:
            self.__available__ = False
            self.rate -= 1
