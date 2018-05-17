# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from bson import InvalidDocument
from scrapy import log
from scrapy.exceptions import DropItem

from yikeitemgrep.items import PaperItem, ModelItem


class MongoPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient('10.200.2.212', 27017)
        db = client['ekwing']
        self.paper = db['zy_papers']
        self.model = db['zy_models']


    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(mongo_uri=crawler.settings.get("MONGO_URI"),
    #                mongo_db=crawler.settings.get("MONGO_DATABASE", "items"))
    #
    # def open_spider(self, spider):
    #     self.client = pymongo.MongoClient(self.mongo_uri)
    #     self.db = self.client[self.mongo_db]
    #
    # def close_spider(self, spider):
    #     self.client.close()

    def process_item(self, item, spider):
        try:
            if isinstance(item, PaperItem):
                self.paper.insert(dict(item))
            elif isinstance(item, ModelItem):
                self.model.insert(dict(item))
            return item
        except InvalidDocument as e:
            log.msg('show items : {}'.format(item))



# item 去重

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['origin_id'] in self.ids_seen:
            pass
            # raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['origin_id'])
            return item


