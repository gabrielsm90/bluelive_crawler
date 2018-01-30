# -*- coding: utf-8 -*-

from dao.mongo import SubmissionsMongoDAO


class MongoWriterPipeline(object):

    def open_spider(self, spider):
        self.mongo_connection = SubmissionsMongoDAO()

    def close_spider(self, spider):
        self.mongo_connection.close_connection()

    def process_item(self, item, spider):
        self.mongo_connection.insert_update_submission(item)
        return item
