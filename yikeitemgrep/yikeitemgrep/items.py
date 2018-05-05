# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PaperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    paper_id = scrapy.Field()
    paper_title = scrapy.Field()


if __name__ == '__main__':
    paper = PaperItem(paper_id='12345')
    print id(paper)
    paper2 = PaperItem(paper)
    print id(paper2)
