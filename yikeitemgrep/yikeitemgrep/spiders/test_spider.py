#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 上午11:35

import json
import re
import urllib

import scrapy
from scrapy import Spider, Request
from scrapy.http.cookies import CookieJar

cookie_jars = CookieJar()


class EkwingSpider(Spider):
    name = 'ekwing_test'
    allowed_domains = ['ekwing.com']

    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "www.ekwing.com/login/view"
    }

    def __init__(self, *args, **kwargs):
        self.province_dict = dict()
        self.base_paper_pages_header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
                                        'Referer': 'https://www.ekwing.com/exam/special/papergenerate'}
        super(EkwingSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        headers = {"Accept": "*/*", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36", "Referer": "www.ekwing.com/login/view"}
        return [
            Request("https://passport.ekwing.com/index/login?callback=jQuery172028761594192983286_1525513573276&uname=78240037&pw=pjGwaDtMogr0lrFNPjmE9i7wiVGq4P1%2B0iiRVtrx6bvLK1YSvoth1LOGmxSAuGow3qcYP7HZZZ3E1ToVqvus0OVhLHb8orlGMTCNtdmd8YW6RUSKxOkY7516CQX2KrzuIpKrzZXtrMxN8HYFBBzEEnCX1hvgVDttpI8OBDrJmbI%3D&client_type=web&encrypt_key=3ffb3a92f1c4d3a388d9e00e707636a3&encrypt_type=rsa&utype=1&mem_type=2&_=1525513788306", headers=headers, callback=self.check_login)
        ]

    def check_login(self, response):
        # 使用extract_cookies方法可以提取response中的cookie
        cookie_jars.extract_cookies(response, response.request)
        with open('cookie.txt', 'w') as f:
            for cookie in cookie_jars:
                f.write(str(cookie) + '\n')

        filter_paper_form_data = {"publish_type": 0, "grade": 0, "grade_type": 3, "special_type": 2, "province_id": 107, "exam_type": 1, "level": 0, "model_type_publish": -1, "paper_type": 0, "ext[name_id]": None, "client_type": 0, "paper_year": 0, "province_name": "\\u7ffc\\u8bfe\\u7f51"}
        get_paper_models_form = {
            'page_from': 'special',
            'paper_id': '101804',
            'search_params': json.dumps(filter_paper_form_data)
        }

        login_cookie = self.load_cookies()
        yield scrapy.FormRequest("https://www.ekwing.com/exam/special/ajaxgetmodellist",
                                 method="POST",
                                 formdata=get_paper_models_form,
                                 headers=self.base_paper_pages_header,
                                 cookies=login_cookie,
                                 callback=self.get_paper)

    @staticmethod
    def load_cookies():
        with open('cookie.txt', 'r') as f:
            cookie_jar = f.read()
            p = re.compile(r'<Cookie (.*?) for .*?>')
            cookies = re.findall(p, cookie_jar)
            cookies = dict(cookie.split('=', 1) for cookie in cookies)
            return cookies

    def get_paper(self, response):
        print response.body
        pass
