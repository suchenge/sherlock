import os
import re
import concurrent.futures
import pyperclip3 as pc

from lxml import etree

from modules.service.download.picture.processor import Processor
from modules.tools.http_request.http_client import HttpClient

list_path = r'D:\Project\sherlock\data\temp'
save_path = r'D:\Project\sherlock\data\picture_url'
search_url = 'https://www.xrmn02.cc/plus/search/index.asp?keyword=%s&searchtype=titlekeywords'

# dir_list = os.listdir(list_path)
url_list = []
got_list = []


def find_download(title):
    id = re.compile(r'((Vol|No)\.\d+)').findall(title)[0]
    url = search_url % id[0]

    response = HttpClient.get_text(url)
    response = response.replace('<font color=red>', '')
    response = response.replace('%s</font>', '')

    html = etree.HTML(response)
    link_list = html.xpath("//div[@class='sousuo']/div[@class='title']/h2/a")

    for link in link_list:
        name = link.findtext('span').split(' ')[0].replace('vol', 'Vol').replace('no', 'No')
        href = 'https://www.xrmn02.cc/%s' % link.get('href')

        if name == title:
            got_list.append(href)

            processor = Processor(href, save_path)
            processor.download()
            os.rmdir(os.path.join(list_path, title))


def batch_search(*keyword):
    picture_links = []
    picture_content = ''

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        link_groups = executor.map(search, keyword)

    for link_group in link_groups:
        for link in link_group:
            print(link)
            picture_content += link + '\n'
            picture_links.append(link)

    pc.copy(picture_content)
    return picture_links

def batch_search2(*keyword):
    picture_links = []
    picture_content = ''

    for kw in keyword:
        link_group = search(kw)

        for link in link_group:
            print(link)
            picture_content += link + '\n'
            picture_links.append(link)

    pc.copy(picture_content)
    return picture_links


def search(keyword):
    url = search_url % keyword
    response = HttpClient.get_text(url)
    html = etree.HTML(response)
    page_links = ['https://www.xrmn02.cc/plus/search/index.asp%s' % link for link in html.xpath("//div[@class='page']/a/@href")]

    picture_links = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        link_groups = executor.map(get_current_page_links, page_links)

    for link_group in link_groups:
        for link in link_group:
            picture_links.append(link)

    return picture_links


def get_current_page_links(url):
    response = HttpClient.get_text(url)
    html = etree.HTML(response)

    link_list = html.xpath("//div[@class='sousuo']/div[@class='title']/h2/a")
    links = []

    for link in link_list:
        href = 'https://www.xrmn02.cc%s' % link.get('href')
        if href not in links:
            links.append(href)
    return links


batch_search('梦梦', '张思允', '玉兔', '久久')
