import os

from download.picture.page_jpmnb import PageJpmnb
from download.picture.page_url import PageUrl

xml_path = os.path.abspath("source_data/picture.xml")
url_list = PageUrl(xml_path).items
for url in url_list:
    page = PageJpmnb(url)
    print(page.url)
    print(page.get_title())
