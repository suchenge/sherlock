import concurrent.futures
from playwright.sync_api import sync_playwright
from modules.tools.http_request.http_client import HttpClient

save_path = 'D:\\'
def download(image):
    HttpClient.download(**image)

def get_mp3(page, title, audio_info):
    page.goto(audio_info['url'])
    page.wait_for_load_state('load')
    mp3_url = page.locator('#jp_audio_0').first.get_attribute('src')

    if mp3_url is not None:
        return {'url': mp3_url, 'path': f'{save_path}/{title}/{audio_info["title"]}.mp3'}
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

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(download, mp3_urls)


if __name__ == '__main__':
    download_mp3('https://www.nianyin.com/tuilixuanyi/1727.html')
