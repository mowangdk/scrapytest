#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 下午5:59


class Question(object):
    def __init__(self, question_id, question_index, question_type, title_text, title_pic, answer, choose_list):
        self.__dict__.update({key: value for key, value in locals().iteritems() if key != 'self'})
