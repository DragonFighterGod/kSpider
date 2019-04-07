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
    str_cookies = 'CONTAINERID=74f8111f821f730b387fb19e850e340bf253651d782d8d4701a76aedd11ce157; UM_distinctid=169f710aa302ec-053aa74cf78fc9-e323069-1fa400-169f710aa3281; skmr-session=XYYKlWFmbwSZIRKqq0ZOLhiYCPYDBiztrouPLaRa1zSq5EoAZ9LktHCA-JI2SPjo1kdaj7zFfb5aY5oxXbKRVetAd_H459RNSyqHRc3EER689w1ib1VYB_SfU_bInlhNWVfXN3vK9hlV16P5bm9J2e0q6e1v7t0P-HVBs56CHiwdLmlOs26Q1IMFj2LM5t-XSxPFLZ6Y3jzpGIudccd9Q5DitMVNAcKssOfrpQyeCqEIPKPNvoN90hV5WsM5O7hnGtvp5oklTrc4QBuJSCHFrmyJSuHRHUDxqxUbBgd_VcJv5_flF8ZIQDtMU-lEiqT2fH4cfN_PspRtVFwqxuWtwcwC3HKMav5OT0WgnaEGx7DWQN4fjBx39IQnjwTjrfhHO6UevZxs0y90kL1Qt5kF-2ECKpvbDL8L9mpWNofGgT5E039q0EJkBAiDZ62T4MUPE24WfVmGQPVo3EiDF3B40iUaFw4kTYCUqCGIKPL9bZRoIXYGZOQ-i3E3rtdbq5CmjWcInvbQ1K1bfaz3VbqYVcowitiYtw5QubCf0gOchOP8ZoL0dftkjUKYVL6GZgpBp0SzYO9TSMXWWwOVPMJrPvGKjKoChw5B21X_LNkQg72VKbG4ulHVuTrmkqXOyLaZ30O54rG7HNJ5zJB1Mjhe6zPYI_j9rkf9jZU9vK4Ei2tNREvMgP2rZEF0K2gbU9sLLkgjQ27NvjICuj3HfKVIw-6uf-SxJCK08wzYfzqDpn6kxCoTIifJDiy54us5hnzG; CNZZDATA1273710201=1555814567-1554623812-null%7C1554627062; SERVERID=36368d874799a34e5708a6a889baa723|1554628299|1554628232'


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
