# -*- coding: utf-8 -*-
import scrapy

from scrapy.spiders import CrawlSpider


class KSpider(scrapy.Spider):
    name = 'k'
    allowed_domains = ['k.com']
    start_urls = ['http://k.com/']

    def parse(self, response):
        pass

