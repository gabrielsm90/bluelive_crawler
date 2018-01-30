# -*- coding: utf-8 -*-

import pymongo


class SubmissionsMongoDAO():

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://public:public@ds119028.mlab.com:19028/news_crawler')
        self.collection = self.client['news_crawler']['submissions']

    def close_connection(self):
        self.client.close()

    def insert_update_submission(self, submission_item):
        filter = {
            'title':submission_item['title'],
            'author':submission_item['author']
        }
        if self.collection.replace_one(filter, dict(submission_item)).modified_count == 0:
            self.collection.insert_one(dict(submission_item))

    def get_10_submissions_point_any_kind(self):
        return list(self.collection.find(projection={'_id': False},
                                         sort=[('punctuation', pymongo.DESCENDING)],
                                         limit = 10))

    def get_10_submissions_point_internal_discussion(self):
        return list(self.collection.find(filter={ 'external_url' : { '$regex' : '^/r/Python/comments' } },
                                         projection={'_id': False},
                                         sort=[('punctuation', pymongo.DESCENDING)],
                                         limit = 10))

    def get_10_submissions_point_external_link(self):
        return list(self.collection.find(filter={ 'external_url' : { '$regex' : '^http' } },
                                         projection={'_id': False},
                                         sort=[('punctuation', pymongo.DESCENDING)],
                                         limit = 10))

    def get_10_submissions_comments_any_kind(self):
        return list(self.collection.find(projection={'_id': False},
                                         sort=[('number_of_comments', pymongo.DESCENDING)],
                                         limit = 10))

    def get_10_submissions_comments_internal_discussion(self):
        return list(self.collection.find(filter={ 'external_url' : { '$regex' : '^/r/Python/comments' } },
                                         projection={'_id': False},
                                         sort=[('number_of_comments', pymongo.DESCENDING)],
                                         limit = 10))

    def get_10_submissions_comments_external_link(self):
        return list(self.collection.find(filter={ 'external_url' : { '$regex' : '^http' } },
                                         projection={'_id': False},
                                         sort=[('number_of_comments', pymongo.DESCENDING)],
                                         limit = 10))




