#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/4 上午11:22

import urllib2
import cookielib


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
    req = urllib2.Request("https://www.ekwing.com/exam/special/papergenerate")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    print response.read()


if __name__ == '__main__':
    # save_cookie_tofile()
    read_cookie_fromfile()