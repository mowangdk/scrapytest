#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 下午5:23
import codecs


class Paper(object):

    def __init__(self, paper_id, title, total_question_count, total_model_count):
        self.__dict__.update({key: value for key, value in locals().iteritems() if key != 'self'})
        self.module_list = list()

    def serialize(self):
        with codecs.open('{}.txt'.format(self.paper_id), 'wr', encoding='utf-8') as paper:
            paper.write(self.title + '\n')
            paper.write((u'总问数: ' + unicode(self.total_question_count) + u'    '))
            paper.write((u'总模块数' + unicode(self.total_model_count) + ' \n'))
            for model in self.module_list:
                model_str = unicode(model)
                paper.write(model_str)

    def model_append(self, model):
        self.module_list.append(model)
