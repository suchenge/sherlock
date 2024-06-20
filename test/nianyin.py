import os
import re
import eyed3
import requests

from ffmpy import FFmpeg
from playwright.sync_api import sync_playwright

from modules.tools.http_request.http_client import HttpClient
from modules.tools.common_methods.unity_tools import format_title, ffmpeg_execute_path
from modules.tools.http_request.request import monitoring
from modules.tools.thread_pools.task import Task
from modules.tools.thread_pools.task_pool import TaskPool

save_path = r'E:\Download'
ffmpeg_path = ffmpeg_execute_path()

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
    format = image['format']

    HttpClient.download(**image)

    if os.path.exists(path):
        new_path = path

        if format is True:
            new_path = path.replace(f'.{image["suffix"]}', '_1.mp3')
            FFmpeg(
                    inputs={path: []},
                    outputs={new_path: []},
                    executable=ffmpeg_path
                  ).run(stdout=None)

        audio_file = eyed3.load(new_path)
        audio_file.initTag()

        audio_file.tag.title = f'{title}-{name}'
        audio_file.tag.album = f'有声小说.{title}'
        audio_file.tag.save()

        if new_path != path:
            os.remove(path)
            os.rename(new_path, path)

def get_mp3(page, audio_info):
    page.goto(audio_info['url'])
    page.wait_for_timeout(2000)
    page.wait_for_load_state('load')
    mp3_url = page.locator('#jp_audio_0').first.get_attribute('src')

    if mp3_url is not None:
        name = re.compile(r'\d+').findall(audio_info['name'])[0].zfill(3)
        url_split = mp3_url.split('.')
        suffix = url_split[len(url_split)-1]
        if suffix is None:
            suffix = 'mp3'

        info = {
                    'url': mp3_url,
                    'title': audio_info['title'],
                    'name': name,
                    'path': f'{save_path}/{audio_info['title']}/{name}.{suffix}',
                    'executor': executor,
                    'format': audio_info['format'],
                    'suffix': suffix
                }
        print(info)

        return info
    else:
        return get_mp3(page, audio_info)


def download_mp3(**kwargs):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        mp3_url = get_mp3(page, kwargs)
        mp3_url['format'] = kwargs['format']
        page.close()
        browser.close()

    download(**mp3_url)


def download_story(main_url):
    format = main_url.startswith('F|')
    url = main_url.replace('F|', '')

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        title = page.locator('xpath=//h1').first.text_content().replace('有声小说', '')
        title = format_title(title)

        audio_list = page.locator('xpath=//div[@class="plist"]/ul/li/a').all()
        audio_urls = []

        for audio_page in audio_list:
            page_url = audio_page.get_attribute('href')
            page_info = {'url': 'https://www.nianyin.com' + page_url, 'title': title, 'name': audio_page.text_content(), 'format': format}
            audio_urls.append(page_info)
            print(page_info)

        page.close()
        browser.close()

        for audio_url in audio_urls:
            # download_mp3(**audio_url)
            TaskPool.append_task(Task(download_mp3, kwargs=audio_url))


if __name__ == '__main__':
    urls = [
        'https://www.nianyin.com/tuilixuanyi/1537.html',
    ]

    TaskPool.set_count(10)

    for url in urls:
        download_story(url)

    TaskPool.join()
