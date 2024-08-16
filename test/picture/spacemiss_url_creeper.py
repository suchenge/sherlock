from lxml import etree
from modules.tools.http_request.http_client import HttpClient


def get_html(url):
    html = HttpClient.get_text(url)
    return etree.HTML(html)

def get_url(url, urls, current_index=0, last_index=0):
    if int(current_index) != 0 and int(last_index) != 0 and int(current_index) >= int(last_index):
        return

    current_html = get_html(url)
    current_urls = current_html.xpath('//h2[@class="entry-title td-module-title"]/a[@rel="bookmark"]/@href')

    for current_url in current_urls:
        if current_url not in urls:
            urls.append(current_url)

    current_page_index = current_html.xpath('//span[@class="current"]/text()')[0]
    current_index = current_page_index

    last_page_title = current_html.xpath('//a[@class="last"]/@title')
    if len(last_page_title) > 0 and last_index == 0:
        last_index = last_page_title[0]

    if int(current_page_index) < int(last_index):
        next_url = current_html.xpath('//a[@aria-label="next-page"]/@href')[0]
        next_url = next_url.split('?')[0]
        get_url(next_url, urls, current_index, last_index)


main_url = 'https://spacemiss.com/brand/xiuren'
url_container = []
current_page_index = 0
last_page_index = 0

get_url(main_url, url_container, current_page_index, last_page_index)

for url in url_container:
    print(url)
