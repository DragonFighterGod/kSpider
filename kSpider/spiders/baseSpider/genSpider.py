#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/3/12'
# qq:2456056533


"""
import scrapy


class GenSpider(scrapy.Spider):

    # override
    name = 'gen'

    # 登录态
    cookies = {}
    str_cookies = ''

    # 可选参数：
    collection_name = ''    # collection_name = spider.name (for mongo)
    need_repet = False      # 默认False(for mysql&& mongo)
    repet_key = ''          # 查询key,限mongo

    allowed_domains = []
    start_urls = []
    base_url = ''


    custom_settings = {'DOWNLOAD_DELAY': 2, 'CONCURRENT_REQUESTS': 12, 'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
                       'DOWNLOADER_MIDDLEWARES': {'kSpider.middlewares.UserAgentDownloaderMiddleware': 543},
                       'ITEM_PIPELINES': {  # 'kSpider.pipelines.CJsonItemPipline': 300,
                           'kSpider.pipelines.BaseMongoPipeline2': 301}}

    # override
    def start_requests(self):
        pass

    # override
    def parse_item(self, response):
        pass

    def string_to_dict(self, str_cookies):  # for cookies
        cookies_dict = {}
        if str_cookies:
            items = str_cookies.split(';')
            for item in items:
                key = item.split('=')[0].replace(' ', '')
                value = item.split('=')[1]
                cookies_dict[key] = value

        return cookies_dict


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(GenSpider)
    process.start()
