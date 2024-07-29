from modules.service.download.picture.creeper import Creeper
from modules.tools.http_request.http_client import HttpClient
from tools.http_request.proxy import Proxies

HttpClient.set_proxies(Proxies())
# 抓取图片程序
Creeper().run()
