#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2018/9/26'
# qq:2456056533


"""
import scrapy
from sqlalchemy import Column, String, Text

from kSpider.db.sqlBase import BaseModel
from kSpider.pipelines import BaseSQLPipeline
from kSpider.spiders.baseSpider.detailSpider import DetailSpider

tydetail_spider = 'tydetail'


class TianyanchaDetailSpider(DetailSpider):
    name = tydetail_spider

    redis_key = 'tyc'

    str_cookies = 'aliyungf_tc=AQAAAG9DKD/cYQcAOc97d2XzcQxh4E53; ssuid=9379214745; csrfToken=HgPWNEkZnaMHamjcrhsuT300; TYCID=d7e5fdf0590a11e9bf866d337a750b3d; undefined=d7e5fdf0590a11e9bf866d337a750b3d; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1554623873; _ga=GA1.2.638468641.1554623874; _gid=GA1.2.2012812491.1554623874; __insp_wid=677961980; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20v; __insp_targlpt=5aSp55y85p_lLeWVhuS4muWuieWFqOW3peWFt1%2FkvIHkuJrkv6Hmga%2Fmn6Xor6Jf5YWs5Y_45p_l6K_iX_W3peWVhuafpeivol%2FkvIHkuJrkv6HnlKjkv6Hmga%2Fns7vnu58%3D; __insp_norec_sess=true; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522zero2%2522%252C%2522integrity%2522%253A%252214%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%2522153%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzc4ODU3MzAyMCIsImlhdCI6MTU1NDYyMzg5NywiZXhwIjoxNTcwMTc1ODk3fQ.96qdjrNO_VIaZLjbTXxAIBvZVb4wOl4v0lCSfLI8qP4yAhkv4VuzLAVeuDaixAx2AU4Cy-xEQFVsXvw6gmigtw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217788573020%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzc4ODU3MzAyMCIsImlhdCI6MTU1NDYyMzg5NywiZXhwIjoxNTcwMTc1ODk3fQ.96qdjrNO_VIaZLjbTXxAIBvZVb4wOl4v0lCSfLI8qP4yAhkv4VuzLAVeuDaixAx2AU4Cy-xEQFVsXvw6gmigtw; _gat_gtag_UA_123487620_1=1; RTYCID=9885f4ef7c1c4858b8ee6c4a06546ae1; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1554624059; __insp_slim=1554624058864; CT_TYCID=0411fa07bbe44682aed396e490191ca3'

    collection_name ='tyc'
    need_repet = True
    repet_key = 'url'

    allowed_domains = ['tianyancha.com']

    custom_settings = DetailSpider.custom_settings.copy()
    custom_settings['DOWNLOAD_DELAY'] = 20
    custom_settings['ITEM_PIPELINES'] = {'kSpider.spiders.tianyancha.tycDetail.TycMysqlPipeline': 301}

    def detail_parse(self, response):
        item = TycItem()
        item['url'] = response.url
        item['logo_ico'] = response.xpath('//div[@class="logo -w100"]/img/@data-src').extract_first()
        item['centent_title'] = response.xpath('//div[@class="header"]/h1/text()').extract_first()

        detail = response.xpath('//div[@class="detail "]')
        item['centent_mobile'] = detail.xpath('div/div/span[2]/text()').extract_first()
        item['centent_email'] = detail.xpath('div/div[2]/span[2]/text()').extract_first()
        item['centent_index'] = detail.xpath('div[2]/div/a/@href').extract_first()
        centent_address = detail.xpath('div[2]/div[2]/span[2]/@title').extract_first()
        if not centent_address:
            centent_address = detail.xpath('div[2]/div[2]/text()').extract_first()
        item['centent_address'] = centent_address

        item['faren'] = response.xpath('//div[@class="humancompany"]/div/a/@title').extract_first()

        tr = response.xpath('//table[@class="table -striped-col -border-top-none"]/tbody')

        d1 = tr.xpath('tr[1]/td[2]/div/text()').extract_first()
        d2 = tr.xpath('tr[1]/td[4]/div/text()').extract_first()

        d3 = tr.xpath('tr[2]/td[2]/text()').extract_first()
        d4 = tr.xpath('tr[2]/td[4]/text()').extract_first()

        d5 = tr.xpath('tr[3]/td[2]/text()').extract_first()
        d6 = tr.xpath('tr[3]/td[4]/text()').extract_first()

        d7 = tr.xpath('tr[4]/td[2]/text()').extract_first()
        d8 = tr.xpath('tr[4]/td[4]/text()').extract_first()

        d9 = tr.xpath('tr[5]/td[2]/span/text()').extract_first()
        d10 = tr.xpath('tr[5]/td[4]/text()').extract_first()

        d11 = tr.xpath('tr[6]/td[2]/text()').extract_first()
        d12 = tr.xpath('tr[6]/td[4]/text()').extract_first()

        d13 = tr.xpath('tr[7]/td[2]/text()').extract_first()
        d14 = tr.xpath('tr[7]/td[4]/text()').extract_first()

        d15 = tr.xpath('tr[8]/td[2]/text()').extract_first()
        d16 = tr.xpath('tr[8]/td[4]/text()').extract_first()

        d17 = tr.xpath('tr[9]/td[2]/text()').extract_first()
        d18 = tr.xpath('tr[9]/td[4]/text()').extract_first()

        d19 = tr.xpath('tr[10]/td[2]/span/span/span[1]/text()').extract_first()

        detail = {'注册资本': d1, '成立日期': d2, '经营状态': d3, '工商注册号': d4, '统一社会信用代码': d5, '组织机构代码': d6, '纳税人识别号': d7,
                  '公司类型': d8, '营业期限': d9, '行业': d10, '纳税人资质': d11, '核准日期': d12, '实缴资本': d13, '人员规模': d14, '参保人数': d15,
                  '登记机关': d16, '注册地址': d17, '英文名称': d18, '经营范围': d19}
        item['detail'] = detail

        item['license'] = ''
        license_url = response.xpath('//div[@id="nav-main-baseInfo"]/a/@href').extract_first()
        if license_url:
            yield scrapy.Request(license_url, callback=self.detail2_parse, cookies=self.cookies, meta={'item': item},
                                 dont_filter=True)
        else:

            yield item

    def detail2_parse(self, response):
        item = response.meta['item']
        item['license'] = response.xpath('//*[@id="web-content"]/div/div/div[1]/div[2]/img/@src').extract_first()

        return item


class TycMysqlPipeline(BaseSQLPipeline):
    def process_item(self, item, spider):
        item = self.clear_item(item)
        _item = TycMysql.db_distinct(self.session,TycMysql, item, item['url'],self.need_repet)
        TycMysql.save_mode(self.session,TycMysql(), _item)
        return _item


class TycItem(scrapy.Item):
    url = scrapy.Field()
    logo_ico = scrapy.Field()
    centent_title = scrapy.Field()
    centent_mobile = scrapy.Field()
    centent_email = scrapy.Field()
    centent_index = scrapy.Field()
    centent_address = scrapy.Field()

    license = scrapy.Field()
    faren = scrapy.Field()
    detail = scrapy.Field()


class TycMysql(BaseModel):
    __tablename__ = 'tianyancha'

    url = Column(String(500))

    logo_ico = Column(String(500))
    centent_title = Column(String(500))
    centent_mobile = Column(String(100))
    centent_index = Column(String(500))
    centent_email = Column(String(100))
    centent_address = Column(String(500))

    license = Column(String(500))
    faren = Column(String(100))
    detail = Column(Text())


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(TianyanchaDetailSpider)
    process.start()
