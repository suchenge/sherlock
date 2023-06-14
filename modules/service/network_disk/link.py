import os
import re

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver


def __01__(content):
    match = re.search('链接[：|:](.*?) 密码[：|:](.*)', content).groups()
    return True, match[0], match[1]

def __02__(content):
    match = re.search('链接：(.*?) \n提取码：(.*)', content).groups()
    return True, match[0], match[1]

def __list__():
    return [__01__, __02__]

class LinkStatus(object):
    normal = "正常",
    resolve = "解析",
    nonexistent = '链接不存在',
    extractfile = '提取文件'

class Link(object):
    def __init__(self, file_path):
        self.__file_path__ = file_path

        self.__url__ = None
        self.__password__ = None
        self.__status__ = LinkStatus.normal
        self.__save_node__ = None

    def __resolve__(self):
        with open(self.__file_path__, 'r') as file:
            content = file.read()

        success = False

        for r in __list__():
            try:
                success, self.__url__, self.__password__ = r(content)

                if success and self.__url__ and self.__password__:
                    break
            except Exception as error:
                pass

        if success is False:
            self.__status__ = LinkStatus.resolve

    @property
    def save_node(self):
        return self.__save_node__

    @save_node.setter
    def save_node(self, node_title: str):
        self.__save_node__ = node_title

    def write(self, browser: WebDriver):
        try:
            self.__resolve__()

            if self.__status__ != LinkStatus.normal:
                raise

            browser.get(self.__url__)
            page_title = browser.title

            if '链接不存在' in page_title:
                self.__status__ = LinkStatus.nonexistent
                raise

            if '请输入提取码' in page_title:
                self.__status__ = LinkStatus.extractfile
                browser.find_element(By.XPATH, "//input[@id='accessCode']").send_keys(self.__password__)
                browser.find_element(By.XPATH, "//div[@id='submitBtn']").submit()

                sleep(2)
                print(browser.title)

                browser.find_element(By.XPATH, "//a[@title='保存到网盘']").click()

                self.__select_save_node__(browser)

                browser.find_element(By.XPATH, "//a[@title='确定']").click()

                if self.__success__(browser):
                    os.rename(self.__file_path__, f'{self.__file_path__}.done')
                else:
                    raise

        except Exception as error:
            os.rename(self.__file_path__, self.__build_file_path_by_status__())

    def __select_save_node__(self, browser):
        if self.__save_node__:
            tree_node_element = browser.find_element(By.XPATH, f"//span[contains(@node-path, '{self.__save_node__}')]//..//..")
            tree_node_element.click()

    def __build_file_path_by_status__(self):
        status = self.__status__

        if type(self.__status__) == tuple:
            status = self.__status__[0]

        file_name = f'{status}.{os.path.basename(self.__file_path__)}.error'
        file_path = os.path.join(os.path.dirname(self.__file_path__), file_name)
        return file_path

    def __success__(self, browser: WebDriver):
        try:
            sleep(2)
            target = browser.find_element(By.XPATH, "//div[@class='info-section-title']")
        except Exception as error:
            return False
        else:
            return target.text == '保存成功'
