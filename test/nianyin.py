import requests
import eyed3
import os
import mutagen

from mutagen.easyid3 import EasyID3
from playwright.sync_api import sync_playwright

from modules.tools.http_request.http_client import HttpClient
from modules.tools.http_request.request import monitoring
from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool
from modules.tools.thread_pools.task_pool_factory import TaskPoolFactory

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

def download(**image):
    path = image['path']
    title = image['title']
    name = image['name']

    HttpClient.download(**image)

    if os.path.exists(path):
        audio_file = eyed3.load(path)
        if audio_file.tag is None:
            audio_file.initTag()

        audio_file.tag.title = f'{title}-{name}'
        audio_file.tag.album = f'{title}'
        audio_file.tag.save()


def get_mp3(page, title, audio_info):
    url = audio_info['url']
    print(url)
    page.goto(url)
    page.wait_for_timeout(2000)
    page.wait_for_load_state('load')
    mp3_url = page.locator('#jp_audio_0').first.get_attribute('src')

    if mp3_url is not None:
        print(mp3_url)
        name = audio_info['title']
        url_split = mp3_url.split('.')
        suffix = url_split[len(url_split)-1]
        if suffix is None:
            suffix = 'mp3'

        info = {
                    'url': mp3_url,
                    'title': title,
                    'name': name,
                    'path': f'{save_path}/{title}/{name}.{suffix}',
                    'executor': executor
                }
        print(info)
        return info
    else:
        return get_mp3(page, title, audio_info)

def format_title(title):
    title = title.replace('\'', '')
    title = title.replace('"', '')
    title = title.replace(':', '')
    return title

def download_mp3(**kwargs):
    title = kwargs['title']
    audio_info = kwargs['audio_info']

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        mp3_url = get_mp3(page, title, audio_info)
        page.close()
        browser.close()

    download(**mp3_url)


def download_story(main_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(main_url)

        title = page.locator('xpath=//h1').first.text_content().replace('有声小说', '')
        title = format_title(title)

        print(title)

        audio_list = page.locator('xpath=//div[@class="plist"]/ul/li/a').all()
        audio_urls = []

        for audio_page in audio_list:
            page_url = audio_page.get_attribute('href')
            page_info = {'url': 'https://www.nianyin.com' + page_url, 'name': title, 'title': audio_page.text_content()}
            audio_urls.append(page_info)
            print(page_info)

        browser.close()

        for audio_url in audio_urls:
            mp3_url = {
                'title': title,
                'audio_info': audio_url
            }

            TaskPool.append_task(Task(download_mp3, kwargs=mp3_url))


if __name__ == '__main__':
    urls = [
        'https://www.nianyin.com/wuxiaxuanhuan/1623.html',
    ]

    for url in urls:
        download_story(url)

    TaskPool.join()
