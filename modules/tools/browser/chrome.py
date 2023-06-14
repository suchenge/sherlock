from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver


class ChromeBrowser(WebDriver):
    def __init__(self):
        service = Service(executable_path=r'D:\Chrome\chromedriver.114.0.5735.90.exe')

        options = Options()
        # 浏览器用户信息
        options.add_argument(r'user-data-dir=D:\Chrome\User Data\0')
        # options.add_argument('--headless')                     # 开启无界面模式
        # options.add_argument("--disable-gpu")                  # 禁用gpu
        # options.add_argument('--user-agent=Mozilla/5.0 HAHA')  # 配置对象添加替换User-Agent的命令
        # options.add_argument('--window-size=1366,768')         # 设置浏览器分辨率（窗口大小）
        # options.add_argument('--start-maximized')              # 最大化运行（全屏窗口）,不设置，取元素会报错
        options.add_argument('--disable-infobars')             # 禁用浏览器正在被自动化程序控制的提示
        # options.add_argument('--incognito')                    # 隐身模式（无痕模式）
        # options.add_argument('--disable-javascript')           # 禁用javascript

        super().__init__(options=options, service=service)
