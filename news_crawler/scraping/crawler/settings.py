# -*- coding: utf-8 -*-

# Scrapy settings for crawler project

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'crawler.pipelines.MongoWriterPipeline': 1,
}

MONGO_URI = 'mongodb://gabriel_menezes:Flu#1902@ds119028.mlab.com:19028/crawler'
MONGO_DATABASE = "crawler"