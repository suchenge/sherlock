import importlib

__settings__ = {
    'xiurenji': 'xiurenji',
    'xiannvku': 'xinannvku',
    'xiuren5': 'xiurenba',
    'xrmn': 'xrmn'
}

def get_module_name(url):
    for key in __settings__.keys():
        if url.find(key) > -1:
            return __settings__[key]
class ResolverStrategyProvider(object):
    @staticmethod
    def build(url, html):
        base_name = 'modules.service.download.picture.strategy'
        module_name = get_module_name(url)
        module = importlib.import_module(f'{base_name}.{module_name}')

        return module.build(url, html)