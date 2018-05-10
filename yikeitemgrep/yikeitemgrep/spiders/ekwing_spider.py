#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 上午11:35
import cookielib
import json
import re
import urllib
import urllib2

import scrapy
from scrapy import Request, Spider
from scrapy.http.cookies import CookieJar

# scrapy 项目处于pycharm项目的子项目， 所以pycharm找不到items， 解决方法是， scrapy项目上右键 --> make_directory_as --> sources root
from yikeitemgrep.items import Province, City

cookie_jar = CookieJar()


class EkwingSpider(Spider):
    name = 'ekwing'
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
        cookie_jar.extract_cookies(response, response.request)
        with open('cookie.txt', 'w') as f:
            for cookie in cookie_jar:
                f.write(str(cookie) + '\n')

        login_cookie = self.load_cookies()
        yield scrapy.Request("https://www.ekwing.com/exam/review/loadmodcity",
                             method="POST",
                             body=urllib.urlencode({'city_id': 1495,
                                                    'page_from': 'special',
                                                    'province_id': 107}),
                             headers=self.base_paper_pages_header,
                             cookies=login_cookie,
                             callback=self.get_all_province)

    @staticmethod
    def load_cookies():
        with open('cookie.txt', 'r') as f:
            cookie_jar = f.read()
            p = re.compile(r'<Cookie (.*?) for .*?>')
            cookies = re.findall(p, cookie_jar)
            cookies = dict(cookie.split('=', 1) for cookie in cookies)
            return cookies

    def save_all_province_city(self, response):
        city_response = json.loads(response.body)
        province_id = city_response['data']['province_id']
        province_name = self.province_dict[province_id]
        all_city_ids = list()
        for city in city_response['data']['city_list']:
            city_instance = City(id=city['id'], city_name=city['name'])
            all_city_ids.append(city['id'])
            yield city_instance

        province_instance = Province(id=province_id, province_name=province_name, city_ids=all_city_ids)
        yield province_instance

    def get_all_province(self, response):

        region_response = json.loads(response.body)
        self.province_dict.update({int(province_data['id']): province_data['name'] for i in region_response['data']['group_list'] for province_data in i['list']})
        login_cookie = self.load_cookies()
        print self.province_dict.keys()
        for province_id in self.province_dict.keys():
            datas = urllib.urlencode({'load_city': 1, 'page_from': 'special', 'province_id': province_id, 'mod': '1525936652656'})
            yield scrapy.Request("https://www.ekwing.com/exam/review/loadmodcity?" + datas,
                                 method="GET",
                                 headers=self.base_paper_pages_header,
                                 cookies=login_cookie,
                                 callback=self.save_all_province_city)
        get_paper_models_form = {
            'model_type': None,
            'page': 1,
            'page_from': 'special',
        }
        for province_id, province_name in self.province_dict.iteritems():
            filter_paper_form_data = {
                'province_id': int(province_id), 'province_name': province_name.encode('utf-8'),
                'client_type': 0, 'exam_type': 1, 'ext[name_id]': None, 'grade': 0, 'grade_type': 3, 'level': 0,
                'model_type_publish': -1, 'paper_type': 0, 'paper_year': 0, 'publish_type': 0, 'special_type': 2
            }
            # 这里有一个问题， 不知道为什么用scrapy.Request发送的请求正常，
            # 但是返回的数据response里面的requestr的province_id 自动变成了0， 导致返回的数据中没有paper_list
            opener = self.urllib2_opener()
            paper_generate = urllib2.Request("https://www.ekwing.com/exam/special/ajaxpapergenerate",
                                             data=urllib.urlencode(filter_paper_form_data),
                                             headers=self.base_paper_pages_header)
            paper_id_response = json.loads(opener.open(paper_generate).read())
            paper_datas = paper_id_response['data']['paper_list']
            for paper in paper_datas:
                paper_id = paper.get('id')
                # paper_id = '124795'
                get_paper_models_form['paper_id'] = str(paper_id)
                get_paper_models_form['search_params'] = json.dumps(filter_paper_form_data)
                yield scrapy.Request("https://www.ekwing.com/exam/special/ajaxgetmodellist?page=1",
                                     method="POST",
                                     body=urllib.urlencode(get_paper_models_form),
                                     headers=self.base_paper_pages_header,
                                     cookies=login_cookie,
                                     callback=self.get_all_items_by_paper_id)
                break

    @staticmethod
    def urllib2_opener():
        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        response = opener.open("https://passport.ekwing.com/index/login?callback=jQuery172028761594192983286_1525513573276&uname=78240037&pw=pjGwaDtMogr0lrFNPjmE9i7wiVGq4P1%2B0iiRVtrx6bvLK1YSvoth1LOGmxSAuGow3qcYP7HZZZ3E1ToVqvus0OVhLHb8orlGMTCNtdmd8YW6RUSKxOkY7516CQX2KrzuIpKrzZXtrMxN8HYFBBzEEnCX1hvgVDttpI8OBDrJmbI%3D&client_type=web&encrypt_key=3ffb3a92f1c4d3a388d9e00e707636a3&encrypt_type=rsa&utype=1&mem_type=2&_=1525513788306")
        return opener

    def get_all_items_by_paper_id(self, response):
        paper_body = json.loads(response.body)
        pass



