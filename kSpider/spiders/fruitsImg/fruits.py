#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/4/3'
# qq:2456056533
"""

import scrapy
import json

from kSpider.items import BaseItem
from kSpider.spiders.baseSpider.genSpider import GenSpider

fruits_spider = 'fruits'


class FruitSpider(GenSpider):
    '''
    百度图片：水果
    '''
    name = fruits_spider
    base_url = "https://image.baidu.com"

    custom_settings = GenSpider.custom_settings.copy()
    custom_settings['ITEM_PIPELINES'] = {'kSpider.pipelines.ImgPipline': 301}

    def start_requests(self):
        urls = [
                {'cate': '苹果',
                  'url': 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%B0%B4%E6%9E%9C%E8%8B%B9%E6%9E%9C&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=%E6%B0%B4%E6%9E%9C%E8%8B%B9%E6%9E%9C&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={page_size}&rn=100'},
                {'cate': '橙子',
                 'url': 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%A9%99%E5%AD%90&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=%E6%A9%99%E5%AD%90&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={page_size}&rn=100'},
                {'cate': '香蕉',
                 'url': 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%B0%B4%E6%9E%9C%E9%A6%99%E8%95%89&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=%E6%B0%B4%E6%9E%9C%E9%A6%99%E8%95%89&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={page_size}&rn=30'},
                {'cate': '火龙果',
                 'url': 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%B0%B4%E6%9E%9C%E7%81%AB%E9%BE%99%E6%9E%9C&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=%E6%B0%B4%E6%9E%9C%E7%81%AB%E9%BE%99%E6%9E%9C&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={page_size}&rn=30'}

                ]

        for url_dict in urls:
            for j in range(30, 6000, 30):
                url = url_dict['url'].format(page_size=j)
                yield scrapy.Request(url, meta={'cate': url_dict['cate']}, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        cate = response.meta['cate']
        data = json.loads(response.text)['data']

        for d in data:
            item = FruitsItem()
            item['name'] = cate
            img_url =''
            if 'hoverURL' in d.keys():
                img_url = d['thumbURL']
                if not img_url and 'middleURL' in d.keys():
                    img_url = d['middleURL']
                if not img_url and 'thumbURL' in d.keys():
                    img_url = d['thumbURL']

            if img_url:
                item['title'] = item.hx_md5(img_url)
                item['img_urls'] = [img_url]
                yield item


class FruitsItem(BaseItem):
    name = scrapy.Field()
    title = scrapy.Field()
    img_urls = scrapy.Field()

if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(FruitSpider)
    process.start()
