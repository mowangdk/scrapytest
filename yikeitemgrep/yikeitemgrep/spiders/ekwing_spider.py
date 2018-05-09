#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 上午11:35
import json
import re
import urllib

import scrapy
from scrapy import Request, Spider
from scrapy.http.cookies import CookieJar

cookie_jar = CookieJar()


class EkwingSpider(Spider):
    name = 'ekwing'
    allowed_domains = ['ekwing.com']

    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "www.ekwing.com/login/view"
    }

    def start_requests(self):
        headers = {"Accept": "*/*", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36", "Referer": "www.ekwing.com/login/view"}
        return [
            Request("https://passport.ekwing.com/index/login?callback=jQuery172028761594192983286_1525513573276&uname=78240037&pw=pjGwaDtMogr0lrFNPjmE9i7wiVGq4P1%2B0iiRVtrx6bvLK1YSvoth1LOGmxSAuGow3qcYP7HZZZ3E1ToVqvus0OVhLHb8orlGMTCNtdmd8YW6RUSKxOkY7516CQX2KrzuIpKrzZXtrMxN8HYFBBzEEnCX1hvgVDttpI8OBDrJmbI%3D&client_type=web&encrypt_key=3ffb3a92f1c4d3a388d9e00e707636a3&encrypt_type=rsa&utype=1&mem_type=2&_=1525513788306", headers=headers, callback=self.check_login)
        ]

    def check_login(self, response):
        # 使用extract_cookies方法可以提取response中的cookie
        cookie_jar.extract_cookies(response, response.request)
        with open('cookie.txt', 'w') as f:
            for cookie in cookie_jar:
                f.write(str(cookie) + '\n')

        all_base_headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                            'Referer': 'https://www.ekwing.com/exam/special/papergenerate'}
        login_cookie = self.load_cookies()
        yield scrapy.Request("https://www.ekwing.com/exam/review/loadmodcity",
                             method="POST",
                             body=urllib.urlencode({'city_id': 1495,
                                                    'page_from': 'special',
                                                    'province_id': 107}),
                             headers=all_base_headers,
                             cookies=login_cookie,
                             callback=self.parse)

    @staticmethod
    def load_cookies():
        with open('cookie.txt', 'r') as f:
            cookie_jar = f.read()
            p = re.compile(r'<Cookie (.*?) for .*?>')
            cookies = re.findall(p, cookie_jar)
            cookies = dict(cookie.split('=', 1) for cookie in cookies)
            return cookies

    def parse(self, response):

        region_response = json.loads(response.body)
        province_list = {province_data['id']: province_data['name'] for i in region_response['data']['group_list'] for province_data in i['list']}




