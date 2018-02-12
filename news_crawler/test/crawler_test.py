# -*- coding: utf-8 -*-

import pytest
import pymongo
from scrapy.crawler import CrawlerProcess
from twisted.python.failure import Failure
from scraper.spider import SubmissionsSpider

@pytest.fixture
def mongo_db_collection():
    client = pymongo.MongoClient('mongodb://public:public@ds119028.mlab.com:19028/news_crawler')
    db = client['news_crawler']
    return db['submissions']

def run_spider(n):
    crawler = CrawlerProcess()
    crawler.crawl(SubmissionsSpider, n=n)
    crawler.start()

def test_crawler_insertions(mongo_db_collection):
    mongo_db_collection.drop()
    run_spider(2)
    assert mongo_db_collection.find().count() > 0

def test_n_not_integer():
    crawlResult = CrawlerProcess().crawl(SubmissionsSpider, n='String')
    assert isinstance(crawlResult.result, Failure)