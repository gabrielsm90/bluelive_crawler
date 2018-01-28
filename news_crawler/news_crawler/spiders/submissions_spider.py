import scrapy
from news_crawler.items import SubmissionItem

class SubmissionsSpider(scrapy.Spider):

    name = "submissions"

    def __init__(self, n):
        if not isinstance(n, int):
            raise TypeError("N must be an integer value")
        super().__init__(self)
        self.start_urls = ['https://www.reddit.com/r/Python/']
        self.n = n
        self.current_page = 0

    def parse(self, response):
        for submission in response.css('div.thing'):
            yield SubmissionItem(
                title = submission.css('a.title.may-blank::text').extract_first(),
                external_url = submission.css('::attr(data-url)').extract_first(),
                internal_url = submission.css('::attr(data-permalink)').extract_first(),
                author = submission.css('::attr(data-author)').extract_first(),
                punctuation = submission.css('::attr(data-score)').extract_first(),
                creation_date = submission.css('p.tagline time.live-timestamp::attr(title)').extract_first(),
                number_of_comments = submission.css('::attr(data-comments-count)').extract_first()
            )
        self.current_page += 1
        if self.current_page < self.n:
            for href in response.css('span.next-button a'):
                yield response.follow(href, callback=self.parse)