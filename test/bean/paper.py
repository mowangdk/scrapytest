#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 下午5:23


class Paper(object):

    def __init__(self, paper_id, title, total_question_count, total_model_count):
        self.__dict__.update({key: value for key, value in locals().iteritems() if key != 'self'})

    def serialize(self):
        with open('{}.txt'.format(self.title + self.paper_id), 'wr') as paper:
            paper.writelines(self.title)
            paper.write('问题总数:' + self.total_question_count)
            paper.write('模块总数:' + self.total_model_count)
