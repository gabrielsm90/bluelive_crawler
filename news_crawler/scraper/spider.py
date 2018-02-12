# -*- coding: utf-8 -*-

import scrapy
from scraper.item import SubmissionItem
import json

class SubmissionsSpider(scrapy.Spider):

    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipeline.MongoWriterPipeline': 200
        }
    }

    def __init__(self, n):
        if not isinstance(n, int):
            raise TypeError("N must be an integer value")
        super().__init__(self)
        self.start_urls = ['https://www.reddit.com/r/Python/']
        self.n = n
        self.current_page = 0

    def parse(self, response):
        for submission in response.css('div.thing'):
            item = SubmissionItem(
                title = submission.css('a.title.may-blank::text').extract_first(),
                external_url = submission.css('::attr(data-url)').extract_first(),
                internal_url = submission.css('::attr(data-permalink)').extract_first(),
                author = {"name" : submission.css('::attr(data-author)').extract_first()},
                punctuation = int(submission.css('::attr(data-score)').extract_first()),
                creation_date = submission.css('p.tagline time.live-timestamp::attr(title)').extract_first(),
                number_of_comments = int(submission.css('::attr(data-comments-count)').extract_first())
            )
            comments_page = submission.css('li.first a::attr(href)').extract_first()
            request = scrapy.Request(comments_page, callback=self.get_commenters)
            request.meta['item'] = item
            yield request
        self.current_page += 1
        if self.current_page < self.n:
            for href in response.css('span.next-button a'):
                yield response.follow(href, callback=self.parse)

    def get_commenters(self, response):
        item = response.meta['item']
        commenters = []
        commentarea = response.css('div.commentarea')[0]
        for comment in commentarea.css('p.tagline'):
            commenter = comment.css('a.author.may-blank::text').extract_first()
            if commenter:
                commenters.append(comment.css('a.author.may-blank::text').extract_first())
        item['commenters'] = commenters
        yield item

