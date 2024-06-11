import requests
import concurrent.futures

from playwright.sync_api import sync_playwright

from modules.tools.http_request.http_client import HttpClient
from modules.tools.http_request.request import monitoring
from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool

save_path = 'D:\\'

@monitoring
def executor(*args, **image):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5',
        'Connection': 'keep-alive',
        'Range': 'bytes=0-',
        'Referer': 'https://www.nianyin.com/',
        'Sec-Fetch-Dest': 'audio',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'sec-ch-us': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
    }

    url = image['url']
    response = requests.get(url, headers=headers)
    return response.content

def get_mp3(page, title, audio_info):
    page.goto(audio_info['url'])
    page.wait_for_load_state('load')
    mp3_url = page.locator('#jp_audio_0').first.get_attribute('src')

    if mp3_url is not None:
        return {'url': mp3_url, 'path': f'{save_path}/{title}/{audio_info["title"]}.mp3', 'executor': executor}
    else:
        return get_mp3(page, title, audio_info)

def format_title(title):
    title = title.replace('\'', '')
    title = title.replace('"', '')
    title = title.replace(':', '')
    return title

def download_mp3(main_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(main_url)

        title = page.locator('xpath=//h1').first.text_content().replace('有声小说', '')
        title = format_title(title)
        audio_list = page.locator('xpath=//div[@class="plist"]/ul/li/a').all()
        audio_urls = []
        mp3_urls = []

        for audio_page in audio_list:
            page_url = audio_page.get_attribute('href')
            audio_urls.append({'url': 'https://www.nianyin.com' + page_url, 'title': audio_page.text_content()})

        for audio_url in audio_urls:
            mp3_urls.append(get_mp3(page, title, audio_url))

        browser.close()

        TaskPool.set_count(10)

        for mp3_url in mp3_urls:
            TaskPool.append_task(Task(HttpClient.download, kwargs=mp3_url))

        TaskPool.join()


if __name__ == '__main__':
    download_mp3('https://www.nianyin.com/tuilixuanyi/1727.html')
