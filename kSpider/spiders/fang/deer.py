# -*- coding: utf-8 -*-
import scrapy
import json

from sqlalchemy import Column, String, Text

from kSpider.db.sqlBase import BaseModel
from kSpider.spiders.baseSpider.genSpider import GenSpider
from kSpider.pipelines import BaseSQLPipeline

deer_name = 'deer'


class DeerSpider(GenSpider):
    name = deer_name

    need_repet = True
    repet_key = 'hid'

    cookies = {}
    str_cookies = '登录后的cookies,===> b38ck2icdtlutt94; UM_distinctid=169f6fad96c33d'


    custom_settings = GenSpider.custom_settings.copy()
    # custom_settings['ITEM_PIPELINES'] = {'kSpider.spiders.fang.deer.DeerSQLPipeline': 301}


    base_url = 'https://www.xiaoluxuanfang.com/api'
    json_data = {"filters": [], "query": {"parentKey": "cityCode", "parentValue": "440300", "type": "sell"},
                 "sorts": [{"key": "sort", "value": "{'default':0}"}], "sinceId": 1, "size": 20}

    def start_requests(self):
        self.cookies = self.string_to_dict(self.str_cookies)

        url = self.base_url + '/v4/search/houses'
        yield scrapy.Request(url, callback=self.parse_list, method='POST', body=json.dumps(self.json_data),
                             headers={'Content-Type': 'application/json; charset=utf-8'}, cookies=self.cookies, dont_filter=True)

    def parse_list(self, response):
        resp = json.loads(response.text)
        nextId = resp['nextId']
        results = resp['result']
        for result in results:
            hid = result['id']
            hname = result['name']
            # hid = '5b7f8fe81b4bf7000690c6b5'
            detail_url = self.base_url + '/v2/houses/{hid}'.format(hid=hid)
            yield scrapy.Request(detail_url, callback=self.parse_detail, cookies=self.cookies,
                                 meta={'hid': hid, 'hname': hname}, dont_filter=True)



        # 下一页
        if self.json_data['sinceId'] != nextId:
            self.json_data['sinceId'] = nextId
            yield scrapy.Request(url=response.url, callback=self.parse_list, method='POST',
                                 body=json.dumps(self.json_data),
                                 headers={'Content-Type': 'application/json; charset=utf-8'}, cookies=self.cookies)

    def parse_detail(self, response):
        item = DeerItem()
        item['hid'] = response.meta['hid']
        item['hname'] = response.meta['hname']
        item['detail'] = json.loads(response.text)

        yield item


class DeerItem(scrapy.Item):
    hid = scrapy.Field()
    hname = scrapy.Field()
    detail = scrapy.Field()


class DeerSQLPipeline(BaseSQLPipeline):
    def process_item(self, item, spider):
        item = self.clear_item(item)
        _item = DeerModel.db_distinct(self.session,DeerModel, item, item['hid'],self.need_repet)
        DeerModel.save_mode(self.session,DeerModel(), _item)
        return item


class DeerModel(BaseModel):
    __tablename__ = 'deer'

    '''

    # mysql 表 detail字段 修改设计成 mediumtext,utf8mb4_general_ci

    '''
    hid = Column(String(200))
    hname = Column(String(500))
    detail = Column(Text())

    @staticmethod
    def db_search(session,db_model, keywords):
        '''by hid'''
        return session.query(db_model.hid).filter_by(hid=keywords).first()  # db_model.hid 有问题


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl(DeerSpider)
    process.start()
