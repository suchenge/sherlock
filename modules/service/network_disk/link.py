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
    notexist = '链接不存在',
    extractfile = '提取文件'

class Link(object):
    def __init__(self, file_path):
        self.__file_path__ = file_path

        self.__url__ = None
        self.__password__ = None
        self.__status__ = LinkStatus.normal

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

    def write(self, browser: WebDriver):
        try:
            self.__resolve__()

            if self.__status__ != LinkStatus.normal:
                raise

            browser.get(self.__url__)
            page_title = browser.title

            if '链接不存在' in page_title:
                self.__status__ = LinkStatus.notexist
                raise

            if '请输入提取码' in page_title:
                self.__status__ = LinkStatus.extractfile
                browser.find_element(By.XPATH, "//input[@id='accessCode']").send_keys(self.__password__)
                browser.find_element(By.XPATH, "//div[@id='submitBtn']").submit()

                sleep(2)
                print(browser.title)

                browser.find_element(By.XPATH, "//a[@title='保存到网盘']").click()
                browser.find_element(By.XPATH, "//a[@title='确定']").click()

                if self.__success__(browser):
                    os.rename(self.__file_path__, f'{self.__file_path__}.done')
                else:
                    raise

        except Exception as error:
            os.rename(self.__file_path__, f'{self.__file_path__}.{self.__status__}.error')

    def __success__(self, browser: WebDriver):
        try:
            sleep(2)
            target = browser.find_element(By.XPATH, "//div[@class='info-section-title']")
        except Exception as error:
            return False
        else:
            return target.text == '保存成功'
