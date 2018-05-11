#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/4 上午11:22

import json
import time
import urllib
import urllib2
import cookielib

from test.bean.model import Model, Type1Model, Type7Model
from test.bean.paper import Paper
from test.bean.question import Question


def save_cookie():
    # 声明一个cookiejar对象来保存cookie
    cookie = cookielib.CookieJar()
    # 利用 HTTPCookieProcessor来创建cookie处理器
    handler = urllib2.HTTPCookieProcessor(cookie)
    # 利用handler来构建opener
    opener = urllib2.build_opener(handler)
    # 这里的open方法同urllib2的urlopen方法， 也可以传入request
    response = opener.open('http://www.baidu.com')
    for item in cookie:
        print 'Name = ' + item.name
        print 'Value = ' + item.value


def save_cookie_tofile():
    # 设置保存cookie的文件， 同级目录下的cookie.txt
    filename = 'cookie.txt'
    # 声明一个MozillaCookieJar对象实例来保存cookie， 之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    handler = urllib2.HTTPCookieProcessor(cookie)
    # 通过handler来构建opener
    opener = urllib2.build_opener(handler)
    response = opener.open("https://passport.ekwing.com/index/login?callback=jQuery172028761594192983286_1525513573276&uname=78240037&pw=pjGwaDtMogr0lrFNPjmE9i7wiVGq4P1%2B0iiRVtrx6bvLK1YSvoth1LOGmxSAuGow3qcYP7HZZZ3E1ToVqvus0OVhLHb8orlGMTCNtdmd8YW6RUSKxOkY7516CQX2KrzuIpKrzZXtrMxN8HYFBBzEEnCX1hvgVDttpI8OBDrJmbI%3D&client_type=web&encrypt_key=3ffb3a92f1c4d3a388d9e00e707636a3&encrypt_type=rsa&utype=1&mem_type=2&_=1525513788306")
    print response.read()
    # ignore_discard: save even cookies set to b discard, 即使cookies将被丢弃也将它保存下来
    # save even cookies that have expired the file is over written if it already exists, 如果该文件中cookies已经存在， 则覆盖源文件写入，
    cookie.save(ignore_discard=True, ignore_expires=True)


def read_cookie_fromfile():
    cookie = cookielib.MozillaCookieJar()
    # 从文件中读取cookie内容到变量
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    # 创建请求的request
    # req = urllib2.Request("https://www.ekwing.com/exam/special/papergenerate")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    all_base_headers = \
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
         'Referer': 'https://www.ekwing.com/exam/special/papergenerate'}

    get_all_regions = urllib2.Request("https://www.ekwing.com/exam/review/loadmodcity",
                                      data=urllib.urlencode({'city_id': 1495,
                                                             'page_from': 'special',
                                                             'province_id': 107}),
                                      headers=all_base_headers)

    region_response = json.loads(opener.open(get_all_regions).read())
    province_list = {province_data['id']: province_data['name'] for i in region_response['data']['group_list'] for province_data in i['list']}

    filter_paper_form_data = {
        'province_id': 107, 'province_name': '翼课网',
        'client_type': 0, 'exam_type': 1, 'ext[name_id]': None, 'grade': 0, 'grade_type': 3, 'level': 0,
        'model_type_publish': -1, 'paper_type': 0, 'paper_year': 0, 'publish_type': 0, 'special_type': 2
    }
    paper_model_list_form_data = {
        'model_type': None,
        'page': 1,
        'page_from': 'special',
    }
    paper_generate = urllib2.Request("https://www.ekwing.com/exam/special/ajaxpapergenerate",
                                     data=urllib.urlencode(filter_paper_form_data),
                                     headers=all_base_headers)
    junor_response = json.loads(opener.open(paper_generate).read())
    paper_datas = junor_response['data']['paper_list']
    for paper in paper_datas:
        # paper_id = paper.get('id')
        paper_id = '124797'
        paper_model_list_form_data['paper_id'] = str(paper_id)
        paper_model_list_form_data['search_params'] = json.dumps(filter_paper_form_data)
        model_lists_request = urllib2.Request("https://www.ekwing.com/exam/special/ajaxgetmodellist",
                                              data=urllib.urlencode(paper_model_list_form_data),
                                              headers=all_base_headers)
        model_lists_data = json.loads(opener.open(model_lists_request).read())
        items_data_serialize(paper, model_lists_data['data'])
        break


def items_data_serialize(current_paper, data):
    model_datas = data['model_list']
    paper = Paper(current_paper['id'], current_paper['title'],
                  data['ques_info']['all'], data['total'], current_paper['year'])
    for model_id, model_data in model_datas.iteritems():
        model_type = model_data['model_type']
        if model_type == u'1':
            model = Type1Model(model_id, model_data['model_type'],
                               model_data['model_type_name'], model_data['model_name'], model_data['model_score'],
                               model_data['real_text'], model_data['real_audio'], model_data['intro_text'])
        elif model_type == u'7':
            model = Type7Model(model_id, model_data['model_type'],
                               model_data['model_type_name'], model_data['model_name'], model_data['model_score'],
                               model_data['title'], model_data['title_ques_map'], model_data['chap_info'][0]['intro_text'])
        else:
            model = Model(model_id, model_data['model_type'], model_data['model_type_name'],
                          model_data['model_name'], model_data.get('_ques_num', ''), model_data['model_score'], model_data.get('listen_ori', ''), model_data.get('title_audio', ''))
        # urllib.urlretrieve(model.title_audio, 'audio/{}.mp3'.format(model_id))
        time.sleep(0.5)
        for ques in model_data.get('ques_list', []):
            question = Question(ques['id'], ques.get('ques_index', 1), ques['ques_type'], ques['title_text'], ques['title_pic'], ques['answer'], ques.get('choose_list', []))
            model.ques_append(question)
        paper.model_append(model)
    # paper.serialize()


if __name__ == '__main__':
    save_cookie_tofile()
    read_cookie_fromfile()