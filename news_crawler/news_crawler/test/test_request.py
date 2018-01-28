
import pytest
from news_crawler.spiders.submissions_spider import SubmissionsSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.python.failure import Failure

@pytest.fixture
def crawler():
    return CrawlerProcess(get_project_settings())

def test_crawler_execution(crawler):
    crawler.crawl(SubmissionsSpider, n=2)
    crawler.start()

def test_n_not_integer(crawler):
    crawlResult = crawler.crawl(SubmissionsSpider, n='String')
    assert isinstance(crawlResult.result, Failure)