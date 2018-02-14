# -*- coding: utf-8 -*-

import pymongo
import operator
import os
from bson.son import SON


class SubmissionsMongoDAO():

    """
    This class provides every communication that
    the application has with Mongo Database.
    """

    def __init__(self):
        self._client = pymongo.MongoClient(self._connection_url()) # Connection with the database.
        self._submissions = self._client[os.environ['MONGO_INSTANCE']]['submissions'] # Name of the collection in DB

    def _connection_url(self):
        """
        Builds the url to connect with database with
        data retrieved from environment variables.
        :return: Connection URL with Mongo DB instance.
        """
        user = os.environ['MONGO_USER']
        password = os.environ['MONGO_PASSWORD']
        database_name = os.environ['MONGO_INSTANCE']
        database_url = os.environ['MONGO_URL']
        return 'mongodb://{}:{}@{}/{}'.format(user, password, database_url, database_name)

    def close_connection(self):
        """
        Closes the connection with databse.
        """
        self._client.close()

    def drop_submissions_collection(self):
        """
        Drop currenct collection on Mongo Database.
        """
        self._submissions.drop()

    def submissions_count(self):
        """
        Get the number of documents in Submissions collection.
        :return: Integer with count of documents.
        """
        return self._submissions.find().count()

    def insert_bulk_data(self, data):
        """
        Insert many documents at once in Submissions collection.
        :param data: List of JSON.
        """
        self._submissions.insert_many(data)

    def insert_update_submission(self, submission_item):
        """
        Insert or update an item in the collection. Tries to
        update and if the element is not found, inserts it.
        :param submission_item: Item to be inserted or updated.
        """
        filter = {
            'title':submission_item['title'],
            'author.name':submission_item['author']['name']
        }
        if self._submissions.replace_one(filter, dict(submission_item)).modified_count == 0:
            self._submissions.insert_one(dict(submission_item))

    def get_top_submissions_point_any_kind(self, limit):
        """
        Get X top submissions with highest punctuation of any kind.
        :param limit: Maximum number of submissions that
        must be returned.
        :return: List of dictionaries with top submissions of any kind
        by punctuation.
        """
        return list(self._submissions.find(projection={'_id': False, 'commenters':False},
                                           sort=[('punctuation', pymongo.DESCENDING)],
                                           limit = limit))

    def get_top_submissions_point_internal_discussion(self, limit):
        """
        Get X top internal discussion submissions with highest punctuation.
        :param limit: Maximum number of submissions that
        must be returned.
        :return: List of dictionaries with top internal discussion
        submissions by punctuation.
        """
        return list(self._submissions.find(filter={'external_url' : {'$regex' : '^/r/Python/comments'}},
                                           projection={'_id': False, 'commenters':False},
                                           sort=[('punctuation', pymongo.DESCENDING)],
                                           limit = limit))

    def get_top_submissions_point_external_link(self, limit):
        """
        Get X top external link submissions with highest punctuation.
        :param limit: Maximum number of submissions that
        must be returned.
        :return: List of dictionaries with top external link
        submissions by punctuation.
        """
        return list(self._submissions.find(filter={'external_url' : {'$regex' : '^http'}},
                                           projection={'_id': False, 'commenters':False},
                                           sort=[('punctuation', pymongo.DESCENDING)],
                                           limit = limit))

    def get_top_submissions_comments_any_kind(self, limit):
        """
        Get X top submissions with highest number of comments of any kind.
        :param limit: Maximum number of submissions that
        must be returned.
        :return: List of dictionaries with top submissions of any kind
        by number of comments.
        """
        return list(self._submissions.find(projection={'_id': False, 'commenters':False},
                                           sort=[('number_of_comments', pymongo.DESCENDING)],
                                           limit = limit))

    def get_top_submissions_comments_internal_discussion(self, limit):
        """
        Get X top internal discussion submissions with highest number of comments.
        :param limit: Maximum number of submissions that
        must be returned.
        :return: List of dictionaries with top internal discussion
        submissions by number of comments.
        """
        return list(self._submissions.find(filter={'external_url' : {'$regex' : '^/r/Python/comments'}},
                                           projection={'_id': False, 'commenters':False},
                                           sort=[('number_of_comments', pymongo.DESCENDING)],
                                           limit = limit))

    def get_top_submissions_comments_external_link(self, limit):
        """
        Get X top external link submissions with highest number of comments.
        :param limit: Maximum number of submissions that
        must be returned.
        :return: List of dictionaries with top external link
        submissions by number of comments.
        """
        return list(self._submissions.find(filter={'external_url' : {'$regex' : '^http'}},
                                           projection={'_id': False, 'commenters':False},
                                           sort=[('number_of_comments', pymongo.DESCENDING)],
                                           limit = limit))

    def get_top_submitters(self, limit = None):
        """
        Get the X top submitters.
        :param limit: Maximum number of users that must
        be returned.
        :return: A dictionary where the user name is the key
        and the number of submissions is the value.
        """
        pipeline = [
            {"$group": {"_id": {"author": "$author.name"}, "submission_count": { "$sum": 1}}},
	        {"$sort" : SON([("submission_count", -1), ("_id", 1)])},
            {"$project" : {"_id":0, "submitter":"$_id", "submission_count":1} }
        ]
        if limit:
            pipeline.append({"$limit" : limit})
        return {commenter['submitter']['author']:commenter['submission_count']
                for commenter in self._submissions.aggregate(pipeline)}

    def get_top_commenters(self, limit = None):
        """
        Get the X top commenters.
        :param limit: Maximum number of users that must
        be returned.
        :return: A dictionary where the user name is the key
        and the number of comments is the value.
        """
        pipeline = [
            {"$unwind": "$commenters"},
            {"$group": {"_id": {"commenter": "$commenters"}, "comment_count": { "$sum": 1}}},
	        {"$sort" : SON([("comment_count", -1), ("_id", 1)])},
            {"$project" : {"_id":0, "commenter":"$_id", "comment_count":1}}
        ]
        if limit:
            pipeline.append({"$limit" : limit})
        return {commenter['commenter']['commenter']:commenter['comment_count']
                for commenter in self._submissions.aggregate(pipeline)}

    def get_top_active_users(self, limit):
        """
        Returns the most active users. To measure the activity
        of a user, the application sums the number of comments
        and the number of submissions that the user made.
        :param limit: Maximum number of users that must
        be returned.
        :return: A dictionary where the user name is the key
        and the value is the sum of number of comments and
        number of submissions.
        """
        top_commenters = self.get_top_commenters()
        top_submitters = self.get_top_submitters()
        users = {k: top_commenters.get(k, 0) + top_submitters.get(k, 0) for k in set(top_commenters) | set(top_submitters)}
        return dict(sorted(users.items(), key=operator.itemgetter(1), reverse=True)[:limit])

    def get_submissions_user(self, user_name):
        """
        Returns the submissions made by a user.
        :param user_name: Name of the user.
        :return: List of JSON containing the submission's
        data.
        """
        pipeline = [
            {"$group": {"_id": {"author": "$author",
                                "creation_date":"$creation_date",
                                "external_url":"$external_url",
                                "internal_url":"$internal_url",
                                "number_of_comments":"$number_of_comments",
                                "punctuation":"$punctuation",
                                "title":"$title"}}},
            {"$match": {"_id.author.name":user_name}},
            {"$project": {"_id": 0,
                          "author": "$_id.author",
                          "creation_date": "$_id.creation_date",
                          "external_url": "$_id.external_url",
                          "internal_url": "$_id.internal_url",
                          "number_of_comments": "$_id.number_of_comments",
                          "punctuation": "$_id.punctuation",
                          "title": "$_id.title"}}
        ]
        return list(self._submissions.aggregate(pipeline))


    def get_posts_commented_by_user(self, user_name):
        """
        Returns the submissions commented by a user.
        :param user_name: Name of the user.
        :return: List of JSON containing the submission's
        data.
        """
        pipeline = [
            {"$unwind": "$commenters"},
            {"$match": {"commenters":user_name}}
        ]
        object_ids = set(submission["_id"] for submission in list(self._submissions.aggregate(pipeline)))
        return list(self._submissions.find({"_id" : {"$in" : list(object_ids)}},
                                           projection={'_id': False, 'commenters': False}))