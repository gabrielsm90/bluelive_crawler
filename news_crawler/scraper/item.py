# -*- coding: utf-8 -*-

import scrapy

class SubmissionItem(scrapy.Item):
    title = scrapy.Field()
    external_url = scrapy.Field()
    internal_url = scrapy.Field()
    author = scrapy.Field()
    punctuation = scrapy.Field()
    creation_date = scrapy.Field()
    number_of_comments = scrapy.Field()
