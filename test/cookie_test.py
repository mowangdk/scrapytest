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
    response = opener.open("http://www.baidu.com")
    # ignore_discard: save even cookies set to b discard, 即使cookies将被丢弃也将它保存下来
    # save even cookies that have expired the file is over written if it already exists, 如果该文件中cookies已经存在， 则覆盖源文件写入，
    cookie.save(ignore_discard=True, ignore_expires=True)


def read_cookie_fromfile():
    cookie = cookielib.MozillaCookieJar()
    # 从文件中读取cookie内容到变量
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    # 创建请求的request
    req = urllib2.Request("http://www.baidu.com")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)


if __name__ == '__main__':
    save_cookie_tofile()