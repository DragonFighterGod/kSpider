# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

import hashlib


class BaseItem(scrapy.Item):
    url = scrapy.Field()

    def hx_md5(self, url=None):
        if url:
            md5 = hashlib.md5()
            md5.update(url.encode('utf-8'))
            return md5.hexdigest()
