#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  :  2018/5/7 下午5:59


class Question(object):
    """
    question_info type
    {u'text': u'In 1960.', u'show_name': u'A', u'pic': u'', u'name': u'A'}
    """
    def __init__(self, question_id, question_index, question_type, title_text, title_pic, answer, choose_list):
        self.__dict__.update({key: value for key, value in locals().iteritems() if key != 'self'})

    def __str__(self):
        title_text = u'{ques_index}. {ques_title} \n'.format(ques_index=self.question_index, ques_title=self.title_text)
        chose_data = u'\t' + u'\t'.join([u'{show_name}. {text}'.format(show_name=chose['show_name'], text=chose['text']) for chose in self.choose_list]) + u'\n'
        answer = u' \t 答案： {} \n'.format(self.answer[0][0])
        return title_text + chose_data + answer

