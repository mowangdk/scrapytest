# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    paper_title = scrapy.Field()
    all_question_count = scrapy.Field()
    all_model_count = scrapy.Field()
    paper_year = scrapy.Field()


class ModelItem(scrapy.Item):
    id = scrapy.Field()
    model_type = scrapy.Field()
    model_type_name = scrapy.Field()
    model_name = scrapy.Field()
    model_score = scrapy.Field()
    listen_ori = scrapy.Field()
    title_audio = scrapy.Field()
    question_num = scrapy.Field()


class Province(scrapy.Item):
    id = scrapy.Field()
    province_name = scrapy.Field()
    city_ids = scrapy.Field()


class City(scrapy.Item):
    id = scrapy.Field()
    city_name = scrapy.Field()


if __name__ == '__main__':
    paper = PaperItem(paper_id='12345')
    print id(paper)
    paper2 = PaperItem(paper)
    print id(paper2)

