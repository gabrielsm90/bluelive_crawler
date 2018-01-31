# -*- coding: utf-8 -*-

import pymongo
import operator
from bson.son import SON


class SubmissionsMongoDAO():

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://public:public@ds119028.mlab.com:19028/news_crawler')
        self.collection = self.client['news_crawler']['submissions']

    def close_connection(self):
        self.client.close()

    def insert_update_submission(self, submission_item):
        filter = {
            'title':submission_item['title'],
            'author.name':submission_item['author']['name']
        }
        if self.collection.replace_one(filter, dict(submission_item)).modified_count == 0:
            self.collection.insert_one(dict(submission_item))

    def get_top_submissions_point_any_kind(self, limit):
        return list(self.collection.find(projection={'_id': False, 'commenters':False},
                                         sort=[('punctuation', pymongo.DESCENDING)],
                                         limit = limit))

    def get_top_submissions_point_internal_discussion(self, limit):
        return list(self.collection.find(filter={ 'external_url' : { '$regex' : '^/r/Python/comments' } },
                                         projection={'_id': False, 'commenters':False},
                                         sort=[('punctuation', pymongo.DESCENDING)],
                                         limit = limit))

    def get_top_submissions_point_external_link(self, limit):
        return list(self.collection.find(filter={ 'external_url' : { '$regex' : '^http' } },
                                         projection={'_id': False, 'commenters':False},
                                         sort=[('punctuation', pymongo.DESCENDING)],
                                         limit = limit))

    def get_top_submissions_comments_any_kind(self, limit):
        return list(self.collection.find(projection={'_id': False, 'commenters':False},
                                         sort=[('number_of_comments', pymongo.DESCENDING)],
                                         limit = limit))

    def get_top_submissions_comments_internal_discussion(self, limit):
        return list(self.collection.find(filter={ 'external_url' : { '$regex' : '^/r/Python/comments' } },
                                         projection={'_id': False, 'commenters':False},
                                         sort=[('number_of_comments', pymongo.DESCENDING)],
                                         limit = limit))

    def get_top_submissions_comments_external_link(self, limit):
        return list(self.collection.find(filter={ 'external_url' : { '$regex' : '^http' } },
                                         projection={'_id': False, 'commenters':False},
                                         sort=[('number_of_comments', pymongo.DESCENDING)],
                                         limit = limit))

    def get_top_submitters(self, limit = None):
        pipeline = [
            {"$group": {"_id": {"author": "$author.name"}, "submission_count": { "$sum": 1}}},
	        {"$sort" : SON([("submission_count", -1), ("_id", 1)])},
            {"$project" : {"_id":0, "submitter":"$_id", "submission_count":1} }
        ]
        if limit:
            pipeline.append({"$limit" : limit})
        return {commenter['submitter']['author']:
                    commenter['submission_count'] for commenter in self.collection.aggregate(pipeline)}

    def get_top_commenters(self, limit = None):
        pipeline = [
            {"$unwind": "$commenters"},
            {"$group": {"_id": {"commenter": "$commenters"}, "comment_count": { "$sum": 1}}},
	        {"$sort" : SON([("comment_count", -1), ("_id", 1)])},
            {"$project" : {"_id":0, "commenter":"$_id", "comment_count":1}}
        ]
        if limit:
            pipeline.append({"$limit" : limit})
        return {commenter['commenter']['commenter']:
                         commenter['comment_count'] for commenter in self.collection.aggregate(pipeline)}

    def get_top_active_users(self, limit):
        top_commenters = self.get_top_commenters()
        top_submitters = self.get_top_submitters()
        users = {k: top_commenters.get(k, 0) + top_submitters.get(k, 0) for k in set(top_commenters) | set(top_submitters)}
        return dict(sorted(users.items(), key=operator.itemgetter(1), reverse=True)[:limit])

    def get_posts_user(self, user_name):
        return list(self.collection.find({"author.name":user_name}, projection={'_id': False, 'commenters':False}))

    def get_posts_commented_by_user(self, user_name):
        pipeline = [
            {"$unwind": "$commenters"},
            {"$match": {"commenters":user_name}},
            {"$project": {"_id": 0}}
        ]
        return list(self.collection.aggregate(pipeline))
