from modules.framework.configuration_manager.configuration_setting import configuration_setting


def find_configuration_node(json_setting, name):
    for website in json_setting:
        if website['name'] == name:
            return website['url']


@configuration_setting('../config/movie-website.json', key='website_base_url',
                       find_node_handler=lambda json: find_configuration_node(json, 'default'))
class TestConfig(object):
    def __init__(self, **kwargs):
        self.__p__ = kwargs['path']
        u = kwargs['url']
        self.__setting__ = kwargs['website_base_url']

    def run(self):
        print(self.__setting__)


t = TestConfig(**{'url': 'ddd', 'path': '3333'})
t.run()
