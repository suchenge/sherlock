import os
import time

from playwright.sync_api import sync_playwright
from tools.http_request.request import Request

start_index = 71140
end_index = 72623
current_index = start_index
request = Request()
base_path = '/Users/vito/Downloads/Music/'
base_url = 'https://m.i275.com/play/71/'

def write_file(info):
    path = info["path"]
    url = info["url"]
    source = info["source"]

    content = request.get_content(url)

    if content:
        with open(path, "ab") as file:
            file.write(content)

        os.remove(source)

def write_list():
    index = current_index
    while index <= end_index:
        source_file = base_path + str(index) + ".txt"
        source_url = base_url + str(index) + ".html"

        if os.path.exists(source_file):
            continue

        with open(source_file, "w") as file:
            file.write(source_url)

        index += 1

def download():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        index = current_index
        while index <= end_index:
            source_file = base_path + str(index) + ".txt"

            if not os.path.exists(source_file):
                index += 1
                continue

            with open(source_file, "r") as file:
                source_url = file.read()

            page.goto(source_url)

            title = page.locator('xpath=//h2[@class="episode-name-h2"]').first.text_content()
            url = page.locator('xpath=//audio').first.get_attribute('src')

            download_info = {
                'url': url,
                'path': '/Users/vito/Downloads/Music/' + title + '.m4a',
                'source': source_file,
            }

            write_file(download_info)

            index += 1

            time.sleep(60)

        page.close()
        browser.close()

#write_list()
download()