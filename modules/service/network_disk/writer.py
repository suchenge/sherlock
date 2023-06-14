import os

from modules.service.network_disk import behavior
from modules.tools.browser.chrome import ChromeBrowser
from modules.service.network_disk.link import Link

class Writer(object):
    def write(self):
        browser = ChromeBrowser()
        browser.implicitly_wait(20)

        link_folder = os.path.abspath("../data/pan_links")
        links = [Link(os.path.join(link_folder, file)) for file in os.listdir(link_folder) if file.endswith('.done') is False]

        for link in links:
            link.save_node = '代码'
            link.write(browser)

        browser.close()
