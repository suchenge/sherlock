import re
import ssl
import urllib.request

from lxml import etree


def get_url_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                      'Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    # proxy = "suchenge:suyuan2UnionPay@172.104.70.149:1443"
    # proxy_handler = urllib.request.ProxyHandler({
    #     "https": "https://" + proxy
    # })
    #
    # opener = urllib.request.build_opener(proxy_handler)
    # request = urllib.request.Request(url, headers=headers)
    # response = opener.open(request)

    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)

    return response.read()


def get_page_content(url, decode="utf-8"):
    return get_url_content(url).decode(decode)

def get_info_0(filename):
    url = "https://www.javhoo.org/ja/av/" + filename
    html = get_page_content(url)
    tree = etree.HTML(html)

    title = tree.xpath("//h1/text()")
    picture = tree.xpath("//img[@class='alignnone size-full']/@src")
    stage_photos = tree.xpath("//a[@class='dt-mfp-item']/@href")

    if title and picture:
        return filename.upper().strip(), format_title(title), picture, stage_photos

def get_info_1(filename):
    site = "https://javdb.com"
    url = site + "/search?q=" + filename + "&f=all"

    print("开始访问信息页面:")
    print("url：" + url)
    tree = etree.HTML(get_page_content(url))

    links = tree.xpath("//div[@class='grid-item column']/a/@href")
    uids = tree.xpath("//div[@class='grid-item column']/a/div[@class='uid']/text()")

    if 0 < len(links) == len(uids) > 0:
        index = 0

        if filename in uids:
            index = uids.index(filename)
        else:
            for i in range(len(uids)):
                if uids[i] in filename:
                    index = i
                    break

        if index < 0:
            print("页面中没有查询到信息")
            return None, None, None

        uid = uids[index]

        if index > -1:
            link = links[index]
            print("url：" + site + link)
            tree = etree.HTML(get_page_content(site + link))

            title = tree.xpath("//h2[@class='title is-4']/strong/text()")[-1]
            picture = tree.xpath("//img[@class='video-cover']/@src")[-1]
            stage_photos = tree.xpath("//div[@class='tile-images preview-images']/a[@class='tile-item']/@href")

            if title and picture and uid:
                return uid.upper().strip(), format_title(title), picture, stage_photos
    else:
        print("页面中没有查询到信息")

def format_title(title):
    return re.compile("[?:*'<>/\\\]").sub("", title).strip()




