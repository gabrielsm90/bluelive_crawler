# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scraper.spider import SubmissionsSpider
import sys

if __name__ == "__main__":
    n = int(sys.argv[1])
    crawler = CrawlerProcess()
    crawler.crawl(SubmissionsSpider, n=n)
    crawler.start()