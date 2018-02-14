# -*- coding: utf-8 -*-

import pytest
from scrapy.crawler import CrawlerProcess
from twisted.python.failure import Failure
from scraper.spider import SubmissionsSpider
from dao.mongo import SubmissionsMongoDAO

@pytest.fixture
def mongo_dao():
    return SubmissionsMongoDAO()

def run_spider(n):
    crawler = CrawlerProcess()
    crawler.crawl(SubmissionsSpider, n=n)
    crawler.start()

def test_n_not_integer():
    crawlResult = CrawlerProcess().crawl(SubmissionsSpider, n='String')
    assert isinstance(crawlResult.result, Failure)

@pytest.mark.first
def test_crawler_insertions(mongo_dao):
    mongo_dao.drop_submissions_collection()
    assert mongo_dao.submissions_count() == 0
    run_spider(3)
    assert mongo_dao.submissions_count() > 0