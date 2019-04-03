#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/3/12'
# qq:2456056533


"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlSpider(CrawlSpider):
    name = 'craw'

    allowed_domains = []
    start_urls = []
    base_url = ''
    cookies = {}

    # 可选参数：
    collection_name = ''  # 默认collection_name = spider.name
    need_repet = False  # 默认不查询去重
    repet_key = ''  # 查询key


    custom_settings = {'DOWNLOAD_DELAY': 3, 'CONCURRENT_REQUESTS': 6, 'CONCURRENT_REQUESTS_PER_DOMAIN': 6,
                       'DOWNLOADER_MIDDLEWARES': {'kSpider.middlewares.UserAgentDownloaderMiddleware': 543},
                       'ITEM_PIPELINES': {'kSpider.pipelines.BaseMongoPipeline2': 300, }}

    rules = (Rule(LinkExtractor(allow=r'projects/\d+/.*\.html', restrict_xpaths='//div[@class="project-medium"]'),
                  callback='parse_item', follow=True),

             # next_page
             Rule(LinkExtractor(restrict_xpaths='//div[@class="pager"]/a[contains(.,"»")]')),

             # Rule(LinkExtractor(restrict_xpaths='//div[@class="pager"]/a/last()/@href')),

             )

    def parse_item(self, response):
        pass
