# -*- coding: utf-8 -*-

import pytest
from dao.mongo import SubmissionsMongoDAO

@pytest.fixture
def mongo_dao():
    return SubmissionsMongoDAO()

def assert_execution(result_set, mongo):
    mongo.close_connection()
    assert len(result_set) > 0

def test_get_top_submissions_point_any_kind(mongo_dao):
    assert_execution(mongo_dao.get_top_submissions_point_any_kind(10), mongo_dao)

def test_get_top_submissions_point_internal_discussion(mongo_dao):
    assert_execution(mongo_dao.get_top_submissions_point_internal_discussion(10), mongo_dao)

def test_get_top_submissions_point_external_link(mongo_dao):
    assert_execution(mongo_dao.get_top_submissions_point_external_link(10), mongo_dao)

def test_get_top_submissions_comments_any_kind(mongo_dao):
    assert_execution(mongo_dao.get_top_submissions_comments_any_kind(10), mongo_dao)

def test_get_top_submissions_comments_internal_discussion(mongo_dao):
    assert_execution(mongo_dao.get_top_submissions_comments_internal_discussion(10), mongo_dao)

def test_get_top_submissions_comments_external_link(mongo_dao):
    assert_execution(mongo_dao.get_top_submissions_comments_external_link(10), mongo_dao)

def test_get_top_submitters(mongo_dao):
    assert_execution(mongo_dao.get_top_submitters(10), mongo_dao)

def test_get_top_commenters(mongo_dao):
    assert_execution(mongo_dao.get_top_commenters(10), mongo_dao)

def test_get_top_active_users(mongo_dao):
    assert_execution(mongo_dao.get_top_active_users(10), mongo_dao)

def test_get_posts_user(mongo_dao):
    assert_execution(mongo_dao.get_posts_user('antirabbit'), mongo_dao)

def test_get_posts_commented_by_user(mongo_dao):
    assert_execution(mongo_dao.get_posts_commented_by_user('Disco_Infiltrator'), mongo_dao)