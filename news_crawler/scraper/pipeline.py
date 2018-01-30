# -*- coding: utf-8 -*-

import pymongo


class MongoWriterPipeline(object):

    collection_name = 'submissions'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://public:public@ds119028.mlab.com:19028/news_crawler')
        self.db = self.client['news_crawler']

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
