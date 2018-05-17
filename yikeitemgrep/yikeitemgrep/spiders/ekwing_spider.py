#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 上午11:35
import cookielib
import json
import urllib
import urllib2

import scrapy
from scrapy import Request, Spider
from scrapy.http.cookies import CookieJar

# scrapy 项目处于pycharm项目的子项目， 所以pycharm找不到items， 解决方法是， scrapy项目上右键 --> make_directory_as --> sources root
from yikeitemgrep.items import Province, City, PaperItem, ModelItem

cookie_jar = CookieJar()


class EkwingSpider(Spider):
    name = 'ekwing'
    allowed_domains = ['ekwing.com']

    headers = {
        "Accept": "*/*",
        "Referer": "www.ekwing.com/login/view"
    }

    def __init__(self, *args, **kwargs):
        self.province_dict = dict()
        self.base_paper_pages_header = {'Referer': 'https://www.ekwing.com/exam/special/papergenerate'}
        super(EkwingSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        headers = {"Accept": "*/*", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36", "Referer": "www.ekwing.com/login/view"}
        return [
            Request("https://passport.ekwing.com/index/login?callback=jQuery172028761594192983286_1525513573276&uname=78240037&pw=pjGwaDtMogr0lrFNPjmE9i7wiVGq4P1%2B0iiRVtrx6bvLK1YSvoth1LOGmxSAuGow3qcYP7HZZZ3E1ToVqvus0OVhLHb8orlGMTCNtdmd8YW6RUSKxOkY7516CQX2KrzuIpKrzZXtrMxN8HYFBBzEEnCX1hvgVDttpI8OBDrJmbI%3D&client_type=web&encrypt_key=3ffb3a92f1c4d3a388d9e00e707636a3&encrypt_type=rsa&utype=1&mem_type=2&_=1525513788306", headers=headers, callback=self.check_login)
        ]

    def check_login(self, response):
        """
        :param response:
        :return:
        @url https://passport.ekwing.com/index/login
        @returns items 1 14
        """
        yield scrapy.Request("https://www.ekwing.com/exam/review/loadmodcity",
                             method="POST",
                             body=urllib.urlencode({'city_id': 1495,
                                                    'page_from': 'special',
                                                    'province_id': 107}),
                             headers=self.base_paper_pages_header,
                             callback=self.get_all_province)

    def save_all_province_city(self, response):
        city_response = json.loads(response.body)
        province_id = city_response['data']['province_id']
        province_name = self.province_dict[province_id]
        all_city_ids = list()
        for city in city_response['data']['city_list']:
            city_instance = City(origin_id=city['id'], city_name=city['name'])
            all_city_ids.append(city['id'])
            yield city_instance

        province_instance = Province(origin_id=province_id, province_name=province_name, city_ids=all_city_ids)
        yield province_instance

    def get_all_province(self, response):

        region_response = json.loads(response.body)
        self.province_dict.update({int(province_data['id']): province_data['name'] for i in region_response['data']['group_list'] for province_data in i['list']})
        # for province_id in self.province_dict.keys():
        #     datas = urllib.urlencode({'load_city': 1, 'page_from': 'special', 'province_id': province_id, 'mod': '1525936652656'})
        #     yield scrapy.Request("https://www.ekwing.com/exam/review/loadmodcity?" + datas,
        #                          method="GET",
        #                          headers=self.base_paper_pages_header,
        #                          callback=self.save_all_province_city
        #                          )
        get_paper_models_form = {
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
            # 目前推测是cookie少了一个key(并不是), 经测试， scrapy发送post请求需要调用FormRequest方法， 单独使用request会导致参数错误？
            # 推测可能是urllib.urlencode编码过的body参数多了一些东西，scrapy无法解码, 详情见test_spider
            opener = self.urllib2_opener()
            paper_generate = urllib2.Request("https://www.ekwing.com/exam/special/ajaxpapergenerate",
                                             data=urllib.urlencode(filter_paper_form_data),
                                             headers=self.base_paper_pages_header)
            paper_id_response = json.loads(opener.open(paper_generate).read())
            paper_datas = paper_id_response['data']['paper_list']
            for index, paper in enumerate(paper_datas):
                paper_id = paper.get('id')
                get_paper_models_form['paper_id'] = paper_id
                get_paper_models_form['search_params'] = json.dumps(filter_paper_form_data)
                yield scrapy.FormRequest("https://www.ekwing.com/exam/special/ajaxgetmodellist",
                                         formdata=get_paper_models_form,
                                         headers=self.base_paper_pages_header,
                                         callback=self.get_all_model_by_paper_id)
                if index > 10:
                    break


    @staticmethod
    def urllib2_opener():
        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)
        response = opener.open("https://passport.ekwing.com/index/login?callback=jQuery172028761594192983286_1525513573276&uname=78240037&pw=pjGwaDtMogr0lrFNPjmE9i7wiVGq4P1%2B0iiRVtrx6bvLK1YSvoth1LOGmxSAuGow3qcYP7HZZZ3E1ToVqvus0OVhLHb8orlGMTCNtdmd8YW6RUSKxOkY7516CQX2KrzuIpKrzZXtrMxN8HYFBBzEEnCX1hvgVDttpI8OBDrJmbI%3D&client_type=web&encrypt_key=3ffb3a92f1c4d3a388d9e00e707636a3&encrypt_type=rsa&utype=1&mem_type=2&_=1525513788306")
        return opener

    def get_all_model_by_paper_id(self, response):
        paper_body = json.loads(response.body)
        body_data = paper_body['data']
        model_datas = body_data['model_list']
        paper_instance = PaperItem(origin_id=body_data['base_info']['paper_id'],
                                   paper_title=body_data['title'],
                                   all_model_count=body_data['total'],
                                   all_question_count=paper_body['data'])

        for model_id, model_data in model_datas.iteritems():
            model_instance = ModelItem(origin_id=model_id,
                                       model_score=model_data['model_score'],
                                       model_type=model_data['model_type'],
                                       model_type_name=model_data['model_type_name'],
                                       model_name=model_data['model_name'])
            if model_instance['model_type'] == u'7':
                model_instance['model_ques_title'] = model_data['title']
                model_instance['title_ques_map'] = model_data['title_ques_map']
                model_instance['title_prepare_time'] = model_data['prepare_time']
            elif model_instance['model_type'] == u'1':
                model_instance['article_text'] = model_data['real_text']
                model_instance['article_audio'] = model_data['real_audio']
                model_instance['intro_text'] = model_data['intro_text']
                model_instance['intro_audio'] = model_data['intro_audio']
            elif model_instance['model_type'] == u'204':
                continue
            else:
                model_instance['question_num'] = model_data['_ques_num']
                model_instance['listen_ori'] = model_data['listen_ori']
                model_instance['title_audio'] = model_data['title_audio']
            # model_instance['questions'] = model_data.get('ques_list', [])
            yield model_instance
            yield paper_instance


