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

jdWaterHot_spider = 'jd_waterHot'
jdWaterHot_h5_spider = 'jd_h5waterHot'


class JDSpider(GenSpider):
    '''
    京东热水器评论
    '''
    name = jdWaterHot_spider

    custom_settings = GenSpider.custom_settings.copy()
    custom_settings['ITEM_PIPELINES'] = {'kSpider.spiders.waterHot.jd.JdSQLPipeline': 301}

    collection_name = 'jd_waterHot'
    need_repet = True  # 查询去重
    repet_key = 'cid'

    def start_requests(self):
        page = 0
        maxPage = 3
        # maxPage = 100
        pagesize = 100
        for i in range(page, maxPage):
            url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv9794&productId=6793702&score=0&sortType=5&page={}&pageSize={}&isShadowSku=0&fold=1".format(
                i, pagesize)
            yield scrapy.Request(url, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        data = response.text
        jdata = data[data.index('{'):-2]
        json_data = json.loads(jdata)
        comments = json_data['comments']

        for comment in comments:
            item = JdWaterHotItem()
            item['cid'] = comment['id']
            item['content'] = comment['content']
            item['creationTime'] = comment['creationTime']
            item['score'] = comment['score']
            if 'images' in comment.keys():
                item['images'] = [img['imgUrl'] for img in comment['images']]
            item['productColor'] = comment['productColor']
            # item['productSales'] = comment['productSales']
            item['productSize'] = comment['productSize']
            if 'afterUserComment' in comment.keys():
                afterUserComment = comment['afterUserComment']
                item['after_created_time'] = afterUserComment['created']
                item['after_content'] = afterUserComment['hAfterUserComment']['content']
                if 'replies' in comment.keys():
                    item['replies'] = [re['content'] for re in comment['replies']]
            # print(item)
            yield item


class JDH5Spider(GenSpider):
    '''
    京东热水器评论-h5
    '''
    name = jdWaterHot_h5_spider

    collection_name = 'jd_waterHot'
    need_repet = True
    repet_key = 'cid'

    custom_settings = GenSpider.custom_settings.copy()
    custom_settings['ITEM_PIPELINES'] = {'kSpider.spiders.waterHot.jd.JdSQLPipeline': 301}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Mobile Safari/537.36',
        'Content-Type': 'text/html; charset=utf-8',
        'Referer': 'https://item.m.jd.com/product/6793702.html?extension_id=eyJhZCI6IjE0NzYiLCJjaCI6IjIiLCJza3UiOiI2NzkzNzAyIiwidHMiOiIxNTUyMzY5MDk3IiwidW5pcWlkIjoie1wiY2xpY2tfaWRcIjpcIjM1ZGE3NDBmLTZmNTItNGRhYy1hNjg3LTM1NmI3Y2FmYTQ3NVwiLFwibWF0ZXJpYWxfaWRcIjpcIjM2OTUwODU4MlwiLFwicG9zX2lkXCI6XCIxNDc2XCIsXCJzaWRcIjpcIjlhNmZhNzNmLTliZTktNGI5MS1hZDI1LWM4MGU0M2MzNWRkMFwifSJ9&jd_pop=35da740f-6f52-4dac-a687-356b7cafa475&abt=0'}

    def start_requests(self):
        page = 1
        maxpage = 3
        # maxpage = 100
        for i in range(page, maxpage):
            url = 'https://wq.jd.com/commodity/comment/getcommentlist?callback=skuJDEvalA&sorttype=5&pagesize=10&sceneval=2&score=0&sku=6793702&page={}&t='.format(
                i)
            yield scrapy.Request(url, callback=self.parse_item, headers=self.headers, dont_filter=True)

    def parse_item(self, response):
        resp = response.text
        data = resp[resp.index('{'):-1].replace('true', '1').replace('false', '0')  # for json
        jresp = eval(data)
        comments = jresp['result']['comments']
        # maxpage = jresp['result']['maxPage']

        for comment in comments:
            item = JdWaterHotItem()
            item['cid'] = comment['id']
            item['content'] = comment['content']
            item['creationTime'] = comment['creationTime']
            item['score'] = comment['score']
            if 'images' in comment.keys():
                item['images'] = [img['imgUrl'] for img in comment['images']]
            item['productColor'] = comment['productColor']
            item['productSize'] = comment['productSize']
            if 'afterUserComment' in comment.keys():
                afterUserComment = comment['afterUserComment']
                item['after_created_time'] = afterUserComment['created']
                item['after_content'] = afterUserComment['hAfterUserComment']['content']
                if 'replies' in comment.keys():
                    item['replies'] = [re['content'] for re in comment['replies']]
            # print(item)
            yield item
            # return 1


class JdSQLPipeline(BaseSQLPipeline):
    def process_item(self, item, spider):
        item = self.clear_item(item)

        _item = JdMysql.db_distinct(self.session, JdMysql, item, item['cid'],
                                    self.need_repet)  # self.need_repet => Pipeline open_spider

        JdMysql.save_mode(self.session, JdMysql(), _item)
        return item


class JdWaterHotItem(scrapy.Item):
    cid = scrapy.Field()
    content = scrapy.Field()
    creationTime = scrapy.Field()
    images = scrapy.Field()
    productColor = scrapy.Field()
    productSize = scrapy.Field()
    score = scrapy.Field()
    after_created_time = scrapy.Field()
    after_content = scrapy.Field()
    replies = scrapy.Field()


class JdMysql(BaseModel):
    __tablename__ = 'jd_waterHot'

    cid = Column(String(200))
    content = Column(Text())
    creationTime = Column(String(200))
    images = Column(Text())
    productColor = Column(String(200))
    productSize = Column(String(100))
    score = Column(String(100))
    after_created_time = Column(String(200))
    after_content = Column(Text())
    replies = Column(Text())

    @staticmethod
    def db_search(session, db_model, keywords):
        '''by cid'''
        result = session.query(db_model.id).filter_by(cid=keywords).first()
        return result


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    # process.crawl(JDSpider)
    process.crawl(JDH5Spider)
    process.start()
