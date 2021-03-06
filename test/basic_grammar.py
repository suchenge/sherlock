import unittest
import requests


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://javdb33.com/',
            'Cookie': 'theme=auto; over18=1; _ym_d=1633615771; _ym_uid=163361577147146056; locale=zh; remember_me_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkluQmxNV3A2YUhOSFRVZ3llWGRVWjI5eWJVTjRJZz09IiwiZXhwIjoiMjAyMS0xMC0yOVQwMzo1NDo1NS4wMDBaIiwicHVyIjoiY29va2llLnJlbWVtYmVyX21lX3Rva2VuIn19--a4fc9d154fd862fcafea2558c182187c8bb5b510; _ym_isad=1; _jdb_session=Lwhd0aqrITh18nGnY1Xim7XtRAlg%2Bxxy9KMALBWQAB2usUgnjcJpipZNkvNsECbaTd1UaG04AI6%2BOiFdf8AHd%2Fx79sxP425vEP1UC825U6mTwLlZdYd0gTdVrlymXlbjNoUstszaXZRXR%2BA6ep1Lubgpbg3Ht1eaYB1RpnuM%2FBoO3tLg1NCDcPmvrqcAW4uHvC%2BibE1YlBVHW3k63g7HRfjC8fkKrHrQMpdBB15RpDlEiZ2PaxLRtNeL59hUSAb62LChrnnIYW54eH7yRWjhaZwczXMAJdnU7ywbNPe2%2FYiuQJVhNMGvspj%2FweOPSraxfkvNDUwbzIRLDvQ7A55cEkrWyNo5bEa%2FmR0%2FGdah%2BWj8HDUt7IOh2AREMEH0RgfR9Sg%3D--pQrKHpNvmvw5waYR--%2BhRb3P9XrK4cC%2FLHUJkQvg%3D%3D'
        }

        self.url = "https://javdb33.com/v/agMYq"

        proxy_address = "suchenge:suyuan2UnionPay@jp2.go2https.com"
        self.proxy = {
            "http": "http://" + proxy_address
            , "https": "https://" + proxy_address
        }

    def test_proxy(self):
        response = requests.get(self.url, headers=self.headers, proxies=self.proxy)
        print(response.text)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
