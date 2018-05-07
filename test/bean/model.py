#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 下午5:49


class Model(object):

    def __init__(self, model_id, model_type, model_type_name, model_name, question_num,
                 model_score, listen_ori, ques_type, title_audio):
        self.__dict__.update({key: value for key, value in locals().iteritems() if key != 'self'})


