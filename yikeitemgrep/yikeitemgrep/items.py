# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    origin_id = scrapy.Field()
    paper_title = scrapy.Field()
    all_question_count = scrapy.Field()
    all_model_count = scrapy.Field()
    paper_year = scrapy.Field()


class ModelItem(scrapy.Item):
    origin_id = scrapy.Field()
    model_type = scrapy.Field()
    model_type_name = scrapy.Field()
    model_name = scrapy.Field()
    model_score = scrapy.Field()
    listen_ori = scrapy.Field()
    title_audio = scrapy.Field()
    question_num = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    # part 一个部分可能包括多个小题, 现放到这里了
    model_ques_title = scrapy.Field()
    title_ques_map = scrapy.Field()
    title_prepare_time = scrapy.Field()
    # model 规则的描述
    intro_text = scrapy.Field()
    intro_audio = scrapy.Field()
    # 朗读题的原文和音频
    article_text = scrapy.Field()
    article_audio = scrapy.Field()
    questions = scrapy.Field()


class Province(scrapy.Item):
    origin_id = scrapy.Field()
    province_name = scrapy.Field()
    city_ids = scrapy.Field()


class City(scrapy.Item):
    origin_id = scrapy.Field()
    city_name = scrapy.Field()


if __name__ == '__main__':
    paper = PaperItem(paper_id='12345')
    print id(paper)
    paper2 = PaperItem(paper)
    print id(paper2)

