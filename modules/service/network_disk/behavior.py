from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver


def select_save_node(browser: WebDriver, node_title: str):
    save_path_title = browser.find_element(By.XPATH, "//div[@class='save-path-item']").get_attribute('title')

    if node_title not in save_path_title:
        tree_node_element = browser.find_element(By.XPATH, f"//span[contains(@node-path, '{node_title}')]//..//..")
        tree_node_element.click()

