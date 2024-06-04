import importlib

__settings__ = {
    'xiurenji': 'xiurenji',
    'xiannvku': 'xinannvku',
    'xiuren': 'xrmn',
    'xrmn': 'xrmn',
    'xr': 'xrmn',
    '12378': 'xrmn',
    'spacemiss': 'spacemiss'
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
