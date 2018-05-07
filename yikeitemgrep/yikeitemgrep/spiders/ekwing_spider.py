#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 上午11:35
from scrapy import FormRequest
from scrapy import Request, Spider


class EkwingSpider(Spider):
    name = 'ekwing'
    allowed_domains = ['ekwing.com']

    def start_requests(self):
        return [Request("https://passport.ekwing.com/index/login?callback=jQuery172028761594192983286_1525513573276&uname=78240037&pw=pjGwaDtMogr0lrFNPjmE9i7wiVGq4P1%2B0iiRVtrx6bvLK1YSvoth1LOGmxSAuGow3qcYP7HZZZ3E1ToVqvus0OVhLHb8orlGMTCNtdmd8YW6RUSKxOkY7516CQX2KrzuIpKrzZXtrMxN8HYFBBzEEnCX1hvgVDttpI8OBDrJmbI%3D&client_type=web&encrypt_key=3ffb3a92f1c4d3a388d9e00e707636a3&encrypt_type=rsa&utype=1&mem_type=2&_=1525513788306", callback=self.post_login)]

    def post_login(self, response):
        print 'preparing login'
        return [FormRequest.from_response(response, callback=self.after_login)]

    def after_login(self):
        pass

