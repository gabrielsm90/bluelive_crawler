# -*- coding: utf-8 -*-

import pymongo


class MongoWriterPipeline(object):

    collection_name = 'submissions'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        filter = {
            'title':item['title'],
            'author':item['author']
        }
        if self.db[self.collection_name].replace_one(filter, dict(item)).modified_count == 0:
            self.db[self.collection_name].insert_one(dict(item))
        return item
