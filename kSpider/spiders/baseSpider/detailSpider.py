#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/3/27'
# qq:2456056533


"""
import scrapy
from scrapy_redis_bloomfilter.spiders import RedisSpider
from scrapy_redis_bloomfilter.utils import bytes_to_str


class DetailSpider(RedisSpider):
    name = 'detail_spider'

    redis_key = 'request:spider'

    allowed_domains = []
    start_urls = []
    base_url = ''
    cookies = {}

    custom_settings = {'DOWNLOAD_DELAY': 3, 'CONCURRENT_REQUESTS': 6, 'CONCURRENT_REQUESTS_PER_DOMAIN': 6,
                       'DOWNLOADER_MIDDLEWARES': {'kSpider.middlewares.UserAgentDownloaderMiddleware': 543},
                       'ITEM_PIPELINES': {  # 'kSpider.pipelines.CJsonItemPipline': 300,
                           'kSpider.pipelines.BaseMongoPipeline2': 301}}

    def make_request_from_data(self, data):
        url = bytes_to_str(data, self.redis_encoding)
        return self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        # self.cookies = string_to_dict()  # cookies
        self.logger.info('爬取url==>:%s' % url)
        return scrapy.Request(url, callback=self.detail_parse, cookies=self.cookies)

    def detail_parse(self, response):
        pass


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(DetailSpider)
    process.start()
