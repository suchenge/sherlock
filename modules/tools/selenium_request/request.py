from selenium import webdriver

from modules.framework.configuration_manager.configuration_setting import configuration_setting


@configuration_setting('../../config/webdriver-setting.json', False)
class Request(object):
    def __init__(self, **kwargs):
        options = webdriver.ChromeOptions()
        # prefs = {
        #     'profile.default_content_settings.popups': 0,
        #     'download.default_directory': 'd:\\'
        # }

        settings = kwargs["settings"]
        executable_path = settings["executable_path"]
        prefs = settings["prefs"]
        arguments = settings["arguments"]

        options.add_experimental_option('prefs', prefs)

        for argument in arguments:
            options.add_argument(argument)

        self.__driver__ = webdriver.Chrome(executable_path=executable_path, chrome_options=options)

    def get(self, url):
        return self.__driver__.get(url)

    def download(self, url, path):
        pass