from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver


class ChromeBrowser(WebDriver):
    def __init__(self):
        option = Options()
        #option.add_argument('--headless')
        option.add_argument(r'user-data-dir=C:\Users\vitos\AppData\Local\Google\Chrome\User Data')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('blink-settings=imagesEnabled=false')
        option.add_argument('--disable-gpu')

        service = Service(executable_path=r'D:\Chrome\chromedriver.114.0.5735.90.exe')
        super().__init__(options=option, service=service)
