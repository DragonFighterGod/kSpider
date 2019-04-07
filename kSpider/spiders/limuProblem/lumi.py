#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/4/3'
# qq:2456056533

"""

import scrapy
import os

from kSpider.spiders.baseSpider.genSpider import GenSpider

lumi_spider = 'lumi'

path = os.path.dirname(__file__)
lumi_html_path = os.path.join(path, 'lumi.html')


class LumiSpider(GenSpider):
    '''
    绿米 常见问题

    '''
    name = lumi_spider

    base_url = "http://www.lumiunited.com"

    def start_requests(self):
        yield scrapy.Request('file:///' + lumi_html_path, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        for type in response.xpath('//div[@class="type"]'):
            item = LumiItem()
            item['type'] = type.xpath('text()').extract_first()
            question_answer = []
            for p in type.xpath('p'):
                question = p.xpath('span/text()').extract_first()
                answer = p.xpath('span[2]')
                _answer = answer.xpath('string(.)').extract_first()
                if question:
                    question_answer.append((question, _answer))

            item['question_answer'] = question_answer

            yield item


class LumiItem(scrapy.Item):
    type = scrapy.Field()
    question_answer = scrapy.Field()


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(LumiSpider)
    process.start()
