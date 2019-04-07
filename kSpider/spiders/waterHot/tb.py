#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/3/18'
# qq:2456056533


"""

import json

import scrapy
from sqlalchemy import Column, String, Text

from kSpider.db.sqlBase import BaseModel
from kSpider.spiders.baseSpider.genSpider import GenSpider
from kSpider.pipelines import BaseSQLPipeline

tbWaterHot_spider = 'tb_waterHot'

class TBSpider(GenSpider):
    '''
    天猫热水器评论
    '''
    name = tbWaterHot_spider
    custom_settings = GenSpider.custom_settings.copy()
    custom_settings['ITEM_PIPELINES'] = {'kSpider.spiders.waterHot.tb.TbSqlPipeline': 301}
    # custom_settings['DOWNLOAD_DELAY'] = 6

    collection_name = 'tb_waterHot'
    need_repet = True  # 启用查询去重
    repet_key = 'cid'
    def start_requests(self):
        page = 1
        maxPage = 2
        # maxPage = 100
        for i in range(page, maxPage):
            url = "https://rate.tmall.com/list_detail_rate.htm?itemId=558046492248&spuId=874396241&sellerId=1652490016&order=3&currentPage={}&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098%23E1hvKvvxvcGvUvCkvvvvvjiPRLq9tjYbRFS9sjljPmPhsjiRRFq9zjlhR2zZ0jrmRphvChCvvvmCvpvZ7DK6MQSw7DiacoM5Mvr4BHdLz6krvpvEphR%2Fh2GvpuWcdphvhZ3U913Ovh8wDMuHiLJqWDWQdphvmZC2bBvJvhC9f46CvCEEoiWpBpCvBUsSSfV7%2BF3WWDRjvpvhphhvv8wCvvBvpvpZmphvLhR9FpmFjLEcnhjEKBmAVAQaUExreut%2BCc6OfaAK5zECwhcI0E%2BXaxy0747BhC3qVmHoDOvXVcIUExjxALwp8BpDN%2B3l51rzpziPlWktvpvIphvvvvvvphCvpvs%2FvvC2GZCvjvUvvhBGphvwv9vvBHtvpCQmvvChcuyCvv3vpvoD1Y1JIIyCvvXmp99hetyCvpvVphhvvvvv2QhvCvvvMMGtvpvhphvvv86CvCHUoY9pTpCvBlIpNpZTRFE5286CvvDvpGZpSpCvoNervpvEph8JV29vp225dphvmZC2nCvcvhVB846CvvDvpxOp%2BvCmeE%2FrvpvBohShHCyvpuIB7z6HRFIAXQQ%3D&needFold=0&_ksTS=1552894666346_1590&callback=jsonp1591".format(
                i)
            yield scrapy.Request(url, callback=self.parse_item, dont_filter=True)
    def parse_item(self, response):
        data = response.text
        jdata = data[data.index('{'):-1]
        json_data = json.loads(jdata)
        comments = json_data['rateDetail']['rateList']
        for comment in comments:
            item = TbWaterHotItem()
            item['cid'] = comment['id']
            item['auctionSku'] = comment['auctionSku']
            item['rateDate'] = comment['rateDate']
            item['pics'] = [img for img in comment['pics']]
            item['rateContent'] = comment['rateContent']
            item['reply'] = comment['reply']
            appendComment = comment['appendComment']
            if appendComment:
                item['commentTime'] = appendComment['commentTime']
                item['content'] = appendComment['content']
            yield item

class TbWaterHotItem(scrapy.Item):
    cid = scrapy.Field()
    auctionSku = scrapy.Field()  # 颜色分类
    rateDate = scrapy.Field()  # 评论时间
    pics = scrapy.Field()  # 评论图片
    reply = scrapy.Field()  # 回复
    rateContent = scrapy.Field()  # 评论
    commentTime = scrapy.Field()  # 追评时间
    content = scrapy.Field()  # 追评

class TbSqlPipeline(BaseSQLPipeline):
    def process_item(self, item, spider):
        item = self.clear_item(item)
        _item = TbModel.db_distinct(self.session,TbModel, item, item['cid'],self.need_repet)
        TbModel.save_mode(self.session,TbModel(), _item)
        return item

class TbModel(BaseModel):

    __tablename__ = 'tb_waterHot'

    cid = Column(String(200))
    auctionSku = Column(String(500))  # 颜色分类
    rateDate = Column(String(200))  # 评论时间
    pics = Column(Text())   # 评论图片
    reply = Column(Text())  # 回复
    rateContent = Column(Text())  # 评论
    commentTime = Column(String(200))  # 追评时间
    content = Column(Text())   # 追评

    @staticmethod
    def db_search(session,db_model,keywords):
        '''by cid'''
        result = session.query(db_model.id).filter_by(cid=keywords).first()
        return result


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(TBSpider)
    process.start()
