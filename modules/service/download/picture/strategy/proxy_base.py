from modules.tools.http_request.proxy import Proxies
from modules.tools.http_request.request import Request

from modules.service.download.picture.strategy.base import Base

class ProxyBase(Base):
    def __init__(self, url, html):
        super().__init__(url, html)
        self.__request__ = Request(Proxies())
