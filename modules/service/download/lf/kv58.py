import os
import json
import requests
import concurrent.futures

from pathlib import Path
from modules.tools.http_request.request import monitoring


class Kv58(object):
    def __init__(self):
        self.__main_url__ = 'https://58kv.cn/#/invite?code=DNYQVTPT'
        self.__password__ = '123'
        self.__data_path__ = '/Users/vito/Workspace/projects/sherlock/data/lf/kv58'
        self.__request_url__ = 'https://58kv.cn/api/sys/lady/page?nameLadyid=&page=%s&limit=100&ladytype=1&accuracy=&dimension=&adcode=%s'
        self.__cities__ = []
        self.__authorization__ = None
        self.__headers__ = None

        self.__get_city__()
        self.__get_authorization__()
        self.__get_headers__()

    @monitoring
    def __download__(self, file):
        path = file.get('path')
        url = file.get('url')

        if path and url:
            folder = os.path.dirname(path)

            if not os.path.exists(folder):
                Path(folder).mkdir(parents=True, exist_ok=True)

        if '.poker' in url:
            headers = {
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5",
                "access-control-request-headers": "cache-control",
                "access-control-request-method": "GET",
                "connection": "keep-alive",
                "host": "cdn.wuyuepai.com",
                "origin": "https://58kv.cn",
                "referer": "https://58kv.cn/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "cross-site",
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
            }

            response = requests.options(url, headers=headers)
        else:
            response = requests.get(url)

        response.encoding = 'utf-8'
        content = response.content

        if content:
            with open(path, "ab") as file:
                file.write(content)

    def __get_headers__(self):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6,zh-TW;q=0.5",
            "authorization": self.__authorization__,
            "priority": "u=1, i",
            "referer": "https://58kv.cn/",
            "sec-ch-ua": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        }
        self.__headers__  = headers

    def __get_authorization__(self):
        response = requests.post('https://58kv.cn/api/sys/user/authalbum', json={
            'albumpwd': '123',
            'invitecode': 'DNYQVTPT',
        }, headers=self.__get_headers__())

        response.encoding = 'utf-8'
        authorization = json.loads(response.text).get('data').get('access_token')
        self.__authorization__ = authorization

    def __get_city__(self):
        with open(self.__data_path__ + '/city.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                city_id = line.split(':')[0]
                self.__cities__.append(city_id)

    def __get_histories__(self, city_id):
        result = []
        file_path = f'{self.__data_path__}/histories/{city_id}.history'

        if not os.path.exists(file_path):
            return result
        else:
            with open(file_path, 'r') as file:
                result = file.read().split(',')

        return result

    def __write_histories__(self, city_id, histories):
        file_path = f'{self.__data_path__}/histories/{city_id}.history'

        with open(file_path, 'w') as file:
            file.write(histories)

    def __append_histories__(self, city_id, histories):
        file_path = f'{self.__data_path__}/histories/{city_id}.history'
        with open(file_path, 'a') as file:
            for line in histories:
                file.write(f',{line}')

    def __write_history__(self, city_id, lady_id):
        file_path = f'{self.__data_path__}/histories/{city_id}.history'
        with open(file_path, 'a') as file:
            file.write(f'{lady_id},')

    def __get_lady_files__(self, item):
        city = item.get('provinceCity')
        region = item.get('region')

        location = ''
        if '-' in city:
            for zone in city.split('-'):
                location += f'{zone}/'
        else:
            location += f'{city}/'

        return f'{self.__data_path__}/{location}{region}'

    def __get_lady__(self, lady):
        '''
        print(f'{lady.get("provinceCity")}-{lady.get("region")}-{lady.get("address")}')
        print(f'{lady.get("titlename")}')
        print(f'{lady.get("characteristics")}')
        '''

        parent_path = self.__get_lady_files__(lady)

        lady_id = lady.get('ladyid')
        title = f'{lady_id}-{lady.get("titlename")}'
        item_folder_path = f'{parent_path}/{title}'

        files = []
        self.__append_files__(files, item_folder_path, lady, 'cover')
        self.__append_files__(files, item_folder_path, lady, 'data')
        self.__append_files__(files, item_folder_path, lady, 'video')

        if len(files) > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                download_result = executor.map(self.__download__, files)

        return lady_id

    def __append_files__(self, files, file_path, item, property_name):
        file_urls = item.get(property_name)

        if file_urls is not None:
            for url in file_urls:
                index = len(files)
                #file_name = url.split('/')[-1].replace('.poker', '.jpg')
                file_name = url.split('/')[-1]
                file_name = f'{str(index).zfill(5)}-{file_name}'
                files.append(
                    {
                        'path': f'{file_path}/{file_name}',
                        'url': url
                    })


    def __get_ladies__(self, city_id, page_count, histories, process_count = 10):
        print()

        line = f'{city_id} - {page_count}'

        url = self.__request_url__ % (page_count, city_id)
        response = requests.get(url,headers=self.__headers__).text
        json_data = json.loads(response)
        data_list = json_data.get('data').get('list')
        total = json_data.get('data').get('total')

        ladies = list(data_list)
        line = f'{line} - {total} - {len(ladies)}'

        print(line)
        print('-------------------------')

        if len(ladies) == 0:
            print(len(histories))
            return False

        lady_group = []
        new_ladies = []
        count = 0

        for lady in ladies:
            lady_id = lady.get('ladyid')
            count = count + 1

            if lady_id not in histories:
                new_ladies.append(lady)

            if len(new_ladies) == process_count or count == len(ladies):
                lady_group.append(new_ladies)
                new_ladies = []

        for group in lady_group:
            with concurrent.futures.ThreadPoolExecutor(max_workers=process_count) as executor:
                get_ladies_result = executor.map(self.__get_lady__, group)

                new_lady_ids = list(get_ladies_result)
                histories.extend(new_lady_ids)
                print(len(histories))
                self.__write_history__(city_id, ','.join(new_lady_ids))

        return True

    @monitoring
    def get(self):
        for city_id in self.__cities__:
            page_count = 1
            histories = self.__get_histories__(city_id)

            while self.__get_ladies__(city_id, page_count, histories=histories):
                page_count += 1

