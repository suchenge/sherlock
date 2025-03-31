import os
import asyncio
import concurrent.futures

from pathlib import Path
from playwright.async_api import async_playwright

from modules.service.download.picture.image import Image
from modules.service.download.picture.url_container import UrlContainer
from modules.tools.http_request.proxy import Proxies
from modules.tools.http_request.request import Request

home_url = r'https://dsws.ok3753682.com/'
source_url_path = os.path.abspath("../../data/picture_url/new.txt")
done_url_path = os.path.abspath("../../data/picture_url/done.txt")
save_path = os.path.abspath("../../data/picture_url/download/")

request = Request(Proxies(), True)
done_container = UrlContainer(done_url_path)
source_container = UrlContainer(source_url_path, True)

def get_urls():
    return open(source_url_path, 'r', encoding='utf-8').readlines()

def deduplication():
    for source_item in source_container.items():
        if source_item.url in done_container.items():
            source_container.remove(source_item)

    source_container.write()

async def get_images(page, url):
    await page.goto(url)
    title = await page.locator("//h1[@id='subject_tpc']").inner_text()
    images = await page.locator("//img[@class='preview-img']").all()

    items = []
    index = 0
    for image in images:
        index = index + 1
        url = await image.get_attribute("data-original")
        image_item = Image(url)
        item = {
            'url': url,
            'path': f'{save_path}/{title}/{str(index).zfill(5)}.{image_item.suffix}',
        }
        items.append(item)
    return items

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(home_url)

        await page.locator("//p[@class='enter-btn']").first.click()

        urls = source_container.items()

        for url in urls:
            try:
                items = await get_images(page, url)

                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    results = executor.map(download_image,items)

                    success_result = [ result for result in results if result is not None]
                    error_results = [ result for result in results if result is None]

                    print(f'下载图片完成，成功{str(len(success_result))}条，失败{(str(len(error_results)))}条')

                    if len(error_results) > 0:
                        raise Exception(f'含有下载出错的记录')

                    done_container.append(url, True)
                    source_container.remove(url, True)
            except Exception as e:
                print(e)

        await page.close()
        await browser.close()

def download_image(item) -> None | str:
    path = item["path"]
    url = item["url"]

    if path and url:
        content = request.get_content(url)

        if content:
            folder = os.path.dirname(path)

            if not os.path.exists(folder):
                Path(folder).mkdir(exist_ok=True)

            with open(path, "ab") as file:
                file.write(content)

            return path

        else:
            print(f'图片[{url}]下载出错')
            return None

asyncio.run(main())