#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 下午5:49


class Model(object):

    def __init__(self, model_id, model_type, model_type_name, model_name, question_num,
                 model_score, listen_ori, title_audio):
        self.__dict__.update({key: value for key, value in locals().iteritems() if key != 'self'})
        self.ques_list = list()

    def ques_append(self, ques):
        self.ques_list.append(ques)

    def __str__(self):
        model_name = u'{}-{} \n'.format(self.model_id, self.model_type_name)
        listen_ori = u'听力原文:    {} \n'.format(self.listen_ori)
        model_score = u'总分: {}'.format(self.model_score)
        ques_str = u'\n\t' + u'\n\t'.join(map(unicode, self.ques_list))
        return u''.join([model_name, listen_ori, model_score, ques_str, u'\n'])


class Type1Model(object):

    def __init__(self, model_id, model_type, model_type_name, model_name, model_score, article_text,
                 article_audio, intro_text):
        self.__dict__.update({key: value for key, value in locals().iteritems() if key != 'self'})
        self.ques_list = list()

    def ques_append(self, ques):
        self.ques_list.append(ques)

    def __str__(self):
        model_name = u'{}-{} \n'.format(self.model_id, self.model_type_name)
        # listen_ori = u'听力原文:    {} \n'.format(self.listen_ori)
        model_score = u'总分: {}'.format(self.model_score)
        intro_text = u'\t\t 题目要求：{} \n'.format(self.intro_text)
        article_text = u'\n\n 题目主文: {} \n'.format(self.article_text)
        ques_str = u'\n\t' + u'\n\t'.join(map(unicode, self.ques_list))
        return u''.join([model_name, intro_text, article_text, model_score, ques_str, u'\n'])


class Type7Model(object):

    def __init__(self, model_id, model_type, model_type_name, model_name, model_score, model_ques_title,
                 model_ques_title_map, intro_text):
        self.__dict__.update({key: value for key, value in locals().iteritems() if key != 'self'})
        self.ques_list = list()

    def ques_append(self, ques):
        self.ques_list.append(ques)

    def __str__(self):
        model_name = u'{}-{} \n'.format(self.model_id, self.model_type_name)
        listen_ori = u'听力原文:    {} \n'.format(self.listen_ori)
        model_score = u'总分: {}'.format(self.model_score)
        ques_str = u'\n\t' + u'\n\t'.join(map(unicode, self.ques_list))
        return u''.join([model_name, listen_ori, model_score, ques_str, u'\n'])
