#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2019/2/23'
# qq:2456056533

"""

import scrapy
import re
from sqlalchemy import Column, String, Text

from kSpider.db.sqlBase import BaseModel
from kSpider.pipelines import BaseSQLPipeline
from kSpider.spiders.baseSpider.genSpider import GenSpider

ajk_name = 'ajk'


class AjkSpider(GenSpider):
    name = ajk_name


    need_repet = True  # 默认False(for mysql&& mongo)
    repet_key = 'url'  # 查询key,限mongo


    custom_settings = GenSpider.custom_settings.copy()
    custom_settings['ITEM_PIPELINES'] = {'kSpider.spiders.fang.anjuke.AjkSQLPipeline': 301}

    # citys = ['hui', 'sz', 'dg']
    citys = ['zq']

    def start_requests(self):
        for c in self.citys:
            url = 'https://{city}.fang.anjuke.com/loupan/all/p1/'.format(city=c)
            yield scrapy.Request(url, meta={'city': c}, callback=self.parse_list,dont_filter=True)

    def parse_list(self, response):
        self.img_identify(response.url)

        city = response.meta['city']
        for mod in response.xpath('//div[@class="infos"]'):
            url = mod.xpath('a/@href').extract_first()
            if url:
                yield response.follow(url, callback=self.parse_detail, meta={'city': city})

        # # 下一页
        # next_page = response.xpath('//div[@class="pagination"]/a[last()]/text()').extract_first()
        # if next_page == '下一页':
        #     next_url = response.xpath('//div[@class="pagination"]/a[last()]/@href').extract_first()
        #     if next_url:
        #         yield scrapy.Request(next_url, callback=self.parse_list, meta={'city': city})

    def parse_detail(self, response):
        item = AjkItem()
        item['url'] = response.url
        item['city'] = response.meta['city']
        base_detail = response.xpath('//div[@class="basic-details"]/div')
        item['name'] = base_detail.xpath('div/div/h1/text()').extract_first()
        item['o_name'] = base_detail.xpath('div/div/p/text()').extract_first()
        tags = base_detail.xpath('div/div/div').xpath('string(.)').extract_first()

        item['tags'] = ''
        if tags:
            tags_list = tags.replace('\n', '').replace(' ', '').split('\r')
            item['tags'] = [tag for tag in tags_list if tag]

        print(item['tags'])
        item['price'] = base_detail.xpath('dl/dd[1]/p/em/text()').extract_first()

        item['open_time'] = base_detail.xpath('dl/dd[2]/span/text()').extract_first()
        item['hand_time'] = base_detail.xpath('dl/dd[3]/span/text()').extract_first()
        item['huxing'] = base_detail.xpath('dl/dd[4]/div').xpath('string(.)').extract_first()
        item['address'] = base_detail.xpath('dl/dd[5]/a/text()').extract_first()
        detail_more_url = response.xpath('//div[@class="more-info"]/a/@href').extract_first()
        item['detail_more_url'] = detail_more_url
        item['tel_sell_house'] = response.xpath('//p[@class="tel clearfix"]/strong/text()').extract_first()

        if detail_more_url:
            yield scrapy.Request(detail_more_url, callback=self.parse_detail_more, meta={'item': item})

    def parse_detail_more(self, response):
        item = response.meta['item']
        # 价格走势
        # price_gy = 'https://chart.anjukestatic.com/loupan/price?loupan_id=411557&type=0&cw=690&ch=250&date=20190224&from=anjuke&v=5'

        # 基本信息拓展
        base_ex_detail = response.xpath('//div[@class="can-border"][1]/ul')
        wy_type = base_ex_detail.xpath('li[4]/div/text()').extract_first()
        item['wy_type'] = ''
        if wy_type == '物业类型':
            wy_type_v = base_ex_detail.xpath('li[4]/div[2]/text()').extract_first()
            item['developer'] = base_ex_detail.xpath('li[5]/div[2]/a/text()').extract_first()
        else:
            wy_type_v = base_ex_detail.xpath('li[5]/div[2]/text()').extract_first()
            item['developer'] = base_ex_detail.xpath('li[6]/div[2]/a/text()').extract_first()

        if wy_type_v:
            item['wy_type'] = wy_type_v

        # 销售信息
        sell_info_xpath = response.xpath('//div[@class="can-item"][2]/div[2]/ul/li')

        item['sell_info'] = self.info(sell_info_xpath)

        # 小区情况
        xq_xpath = response.xpath('//div[@class="can-item"][3]/div[2]/ul/li')

        item['xq_info'] = self.info(xq_xpath)

        # print(item)

        yield item

    def info(self, info_xpath):
        k_inof = []
        v_info = []
        for i in info_xpath:
            k = i.xpath('div/text()').extract_first()
            if k:
                k_inof.append(k)

        for j in info_xpath:
            v = j.xpath('div[2]').xpath('string(.)').extract_first()
            if v:
                v = re.sub('\[查看详情\]', '', v)
                v_info.append(v)

        dict_info = dict(zip(k_inof, v_info))
        return dict_info

    def img_identify(self, url):
        if url.startswith('https://sz.fang.anjuke.com/xinfang/captchaxf-verify/?'):
            from kSpider.spiders.fang.vcode.anjuke.anjuke import action
            self.logger.info(" -------图形验证码-----")
            action()


class AjkSQLPipeline(BaseSQLPipeline):
    def process_item(self, item, spider):
        item = self.clear_item(item)
        _item = AjkModel.db_distinct(self.session,AjkModel, item, item['url'], self.need_repet)
        AjkModel.save_mode(self.session,AjkModel(), _item)
        return item


class AjkItem(scrapy.Item):
    url = scrapy.Field()
    city = scrapy.Field()  # 城市
    name = scrapy.Field()
    o_name = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()  # 参考价格
    open_time = scrapy.Field()  # 开盘日期
    hand_time = scrapy.Field()  # 交房时间
    huxing = scrapy.Field()  # 户型
    address = scrapy.Field()
    detail_more_url = scrapy.Field()  # 详细信息
    tel_sell_house = scrapy.Field()  # 售楼电话

    # detail_more
    wy_type = scrapy.Field()  # 物业类型
    developer = scrapy.Field()  # 开发商
    sell_info = scrapy.Field()  # 售楼情况
    xq_info = scrapy.Field()  # 小区情况


class AjkModel(BaseModel):
    __tablename__ = 'anjuke'


    url = Column(String(500))
    city = Column(String(100))
    name = Column(String(100))
    o_name = Column(String(100))
    tags = Column(String(1000))
    price = Column(String(100))
    open_time = Column(String(100))
    hand_time = Column(String(100))
    huxing = Column(String(500))
    address = Column(String(500))
    detail_more_url = Column(String(500))
    tel_sell_house = Column(String(100))
    wy_type = Column(String(100))
    developer = Column(String(200))
    sell_info = Column(Text())
    xq_info = Column(Text())


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    process = CrawlerProcess(get_project_settings())
    process.crawl(AjkSpider)
    process.start()
