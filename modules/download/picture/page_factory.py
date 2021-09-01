from modules.download.picture.page_jpmnb import PageJpmnb
from modules.download.picture.page_xiurenji import PageXiuRenJi


class PageFactory(object):
    settings = {
        'jpmnb': PageJpmnb
        , 'xiurenji': PageXiuRenJi
    }

    @staticmethod
    def get_instance(url):
        for settingKey in PageFactory.settings.keys():
            if url.find(settingKey) > -1:
                return PageFactory.settings[settingKey]
