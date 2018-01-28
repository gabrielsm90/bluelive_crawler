# -*- coding: utf-8 -*-

# Scrapy settings for news_crawler project

BOT_NAME = 'news_crawler'

SPIDER_MODULES = ['news_crawler.spiders']
NEWSPIDER_MODULE = 'news_crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'news_crawler.pipelines.MongoWriterPipeline': 1,
}

MONGO_URI = 'mongodb://gabriel_menezes:Flu#1902@ds119028.mlab.com:19028/news_crawler'
MONGO_DATABASE = "news_crawler"