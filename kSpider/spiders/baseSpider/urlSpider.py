#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/3/27'
# qq:2456056533

"""
from redis import Redis

from kSpider.spiders.baseSpider.genSpider import GenSpider
from kSpider.settings import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD


class UrlSpider(GenSpider):
    # override
    name = 'url_spider'
    # override
    redis_key = 'url_spider'

    redis = Redis(REDIS_HOST,port=int(REDIS_PORT),password=REDIS_PASSWORD)

    url_count = 0

    # override
    def start_requests(self):
        pass


    def add_url(self, url):
        if url:
            self.url_count = self.redis.lpush(self.redis_key, url)
            # self.url_count = self.redis.sadd(self.redis_key, url)
            self.logger.info('url_count ===>:%s' % self.url_count)
        else:
            self.logger.info('url ===> error: no url')


    ### overried
    def url_parse(self, response):
        self.add_url("url")
        pass



def redis_add_cs():
    redis_key = 'cs'
    redis = Redis(REDIS_HOST, port=int(REDIS_PORT), password=REDIS_PASSWORD)
    status = redis.lpush(redis_key,"test")
    print(status)



if __name__ == '__main__':

    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(UrlSpider)
    process.start()
