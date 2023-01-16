from modules.service.download.picture.page_base import PageBase
from modules.service.download.picture.page_jpmnb import PageJpmnb
from modules.service.download.picture.page_jpxgmn import PageJpxgmn
from modules.service.download.picture.page_xiurenji import PageXiuRenJi
from modules.service.download.picture.page_xiannvku import PageXinannvku
from modules.service.download.picture.page_xiurenba import PageXiurenba


class PageFactory(object):
    settings = {
        'xiurenji': PageXiuRenJi,
        'xiannvku': PageXinannvku,
        'xiurenba': PageXiurenba,
        'jpmnb': PageJpmnb,
        'jpxgmn': PageJpxgmn
    }

    @staticmethod
    def get_instance(url):
        page = PageBase
        for settingKey in PageFactory.settings.keys():
            if url.find(settingKey) > -1:
                page = PageFactory.settings[settingKey]

        if page is None:
            page = PageBase

        return page

