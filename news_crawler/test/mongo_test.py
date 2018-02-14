# -*- coding: utf-8 -*-

import pytest
from dao.mongo import SubmissionsMongoDAO
import sys
from bson import json_util


@pytest.fixture(scope="session")
def mongo_dao():
    return SubmissionsMongoDAO()

@pytest.fixture(scope="session", autouse=True)
def import_test_data(mongo_dao):
    mongo_dao.drop_submissions_collection()
    try:
        import_file = open("data_export", encoding="utf8")
    except:
        import_file = open("news_crawler/test/data_export", encoding="utf8")
    text = json_util.dumps(import_file.readlines())
    import_file.close()
    result = [json_util.loads(submission) for submission in json_util.loads(text)]
    mongo_dao.insert_bulk_data(result)

def assert_execution(result_set, mongo_dao):
    mongo_dao.close_connection()
    assert len(result_set) > 0
    return result_set

def assert_resultset_ordenation(result_set, comparisson_field, ascendent=False):
    current_value = sys.maxsize
    for document in result_set:
        if ascendent:
            assert document[comparisson_field] >= current_value
        else:
            assert document[comparisson_field] <= current_value
        current_value = document[comparisson_field]

def assert_non_duplicated_result_set(result_set):
    result_set_without_duplicated = set(json_util.dumps(dictionary, sort_keys=True) for dictionary in result_set)
    assert len(result_set) == len(result_set_without_duplicated)

def test_get_top_submissions_point_any_kind(mongo_dao):
    result_set = assert_execution(mongo_dao.get_top_submissions_point_any_kind(10), mongo_dao)
    assert_resultset_ordenation(result_set, 'punctuation')

def test_get_top_submissions_point_internal_discussion(mongo_dao):
    result_set = assert_execution(mongo_dao.get_top_submissions_point_internal_discussion(10), mongo_dao)
    assert_resultset_ordenation(result_set, 'punctuation')

def test_get_top_submissions_point_external_link(mongo_dao):
    result_set = assert_execution(mongo_dao.get_top_submissions_point_external_link(10), mongo_dao)
    assert_resultset_ordenation(result_set, 'punctuation')

def test_get_top_submissions_comments_any_kind(mongo_dao):
    result_set = assert_execution(mongo_dao.get_top_submissions_comments_any_kind(10), mongo_dao)
    assert_resultset_ordenation(result_set, 'number_of_comments')

def test_get_top_submissions_comments_internal_discussion(mongo_dao):
    result_set = assert_execution(mongo_dao.get_top_submissions_comments_internal_discussion(10), mongo_dao)
    assert_resultset_ordenation(result_set, 'number_of_comments')

def test_get_top_submissions_comments_external_link(mongo_dao):
    result_set = assert_execution(mongo_dao.get_top_submissions_comments_external_link(10), mongo_dao)
    assert_resultset_ordenation(result_set, 'number_of_comments')

def test_get_top_submitters(mongo_dao):
    result_set_limited = assert_execution(mongo_dao.get_top_submitters(10), mongo_dao)
    full_result_set = assert_execution(mongo_dao.get_top_submitters(), mongo_dao)
    assert max(result_set_limited.values()) == max(full_result_set.values())

def test_get_top_commenters(mongo_dao):
    result_set_limited = assert_execution(mongo_dao.get_top_commenters(10), mongo_dao)
    full_result_set = assert_execution(mongo_dao.get_top_commenters(), mongo_dao)
    assert max(result_set_limited.values()) == max(full_result_set.values())

def test_get_top_active_users(mongo_dao):
    result_set = assert_execution(mongo_dao.get_top_active_users(10), mongo_dao)
    top_commenters = mongo_dao.get_top_commenters()
    top_submitters = mongo_dao.get_top_submitters()
    users = set(top_commenters.get(k, 0) + top_submitters.get(k, 0) for k in set(top_commenters) | set(top_submitters))
    assert max(result_set.values()) == max(users)

def test_get_posts_user(mongo_dao):
    result_set = assert_execution(mongo_dao.get_submissions_user('dan_kilomon'), mongo_dao)
    assert_non_duplicated_result_set(result_set)

def test_get_posts_commented_by_user(mongo_dao):
    result_set = assert_execution(mongo_dao.get_posts_commented_by_user('breamoreboy'), mongo_dao)
    assert_non_duplicated_result_set(result_set)