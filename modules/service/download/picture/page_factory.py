from modules.service.download.picture.page_base import PageBase
from modules.service.download.picture.page_xiurenji import PageXiuRenJi


class PageFactory(object):
    settings = {
        'xiurenji': PageXiuRenJi
        # , 'jpmnb': PageJpmnb
        # , 'jpxgmn': PageJpxgmn
    }

    @staticmethod
    def get_instance(url):
        for settingKey in PageFactory.settings.keys():
            if url.find(settingKey) > -1:
                return PageFactory.settings[settingKey]
            else:
                return PageBase
