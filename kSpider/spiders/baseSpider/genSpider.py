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
    name = 'gen'

    allowed_domains = []
    start_urls = []
    base_url = ''
    cookies = {}

    # 可选参数：
    collection_name = ''  # collection_name = spider.name
    need_repet = False  # 默认False
    repet_key = ''  # 查询key

    custom_settings = {'DOWNLOAD_DELAY': 2, 'CONCURRENT_REQUESTS': 12, 'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'DOWNLOADER_MIDDLEWARES': {'kSpider.middlewares.UserAgentDownloaderMiddleware': 543},
        'ITEM_PIPELINES': {#'kSpider.pipelines.CJsonItemPipline': 300,
                           'kSpider.pipelines.BaseMongoPipeline2': 301}}

    def start_requests(self):
        pass

    def parse_item(self, response):
        pass


def string_to_dict():  # for cookies
    cookies = 'QCCSESSID=tjl02vg0gref2sh7qdgo7d5tv1; UM_distinctid=16908a4761f6d6-006afca38281ca-b781636-1fa400-16908a47620171; CNZZDATA1254842228=607620362-1550623808-https%253A%252F%252Fwww.baidu.com%252F%7C1550623808; zg_did=%7B%22did%22%3A%20%2216908a47b97321-0eb46a2d70dfe4-b781636-1fa400-16908a47b983de%22%7D; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1550628191; hasShow=1; _uab_collina=155062819187986042757468; acw_tc=0e77721515506281902036981e0cee085aaf3bc2ad03ce07fdbeb4f943; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1550628264; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201550628191131%2C%22updated%22%3A%201550628274118%2C%22info%22%3A%201550628191135%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%22265d30ecc365058984801223ceaf0330%22%7D'
    cookies_dict = {}
    items = cookies.split(';')
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
