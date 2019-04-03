#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2019/2/22'
# qq:2456056533

"""
import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
from scrapy import Item
import logging
import pymongo

from kSpider.db.config import HOST, MONGO_PORT, MONGO_USER, MONGO_ADMIN_PWD, DB_NAME


class MongoHandler:
    '''
     mongo异步操作
    '''

    def __init__(self, collection_name='default', host=HOST, port=MONGO_PORT, user=MONGO_USER, pwd=MONGO_ADMIN_PWD,db=DB_NAME):
        self.client = AsyncIOMotorClient('mongodb://{user}:{pwd}@{host}:{port}/'.format(user=user,pwd=pwd,host=host,port=port))
        self.db = self.client[db]
        self.collection_name = collection_name  # logging
        self.collection = self.db[collection_name]

        # self.loop = asyncio.new_event_loop()    # different loop
        self.loop = asyncio.get_event_loop()

    async def process(self, item, repet_key, need_repet, repet_value):

        if isinstance(item, Item):
            item_data = item.__dict__['_values']
        elif isinstance(item, dict):
            item_data = item
        else:
            try:
                item_data = json.loads(item)
            except:
                raise ('******************** item must dict ')

        repet = await self.find(repet_key, need_repet, repet_value)

        if not repet:
            if await self.collection.insert_one(item_data):
                logging.info('********************save to mongodb_{collection}==> success:\n{item}'.format(
                    collection=self.collection_name, item=item_data))
            else:
                raise ('********************save to mongodb_{collection}==> fail:\n{item}'.format(
                    collection=self.collection_name, item=item_data))
        else:
            logging.info(
                '********************mongodb_{collection}==> repet :\n{item}'.format(collection=self.collection_name,
                                                                                     item=item_data))

    async def find(self, repet_key, need_repet, repet_value):
        '''可选的mongo查询去重
            need_repet: 默认False不去重
            repet_key:  查询key
            repet_value: 对应的value
        '''
        if not need_repet: return False
        repet_data = await self.collection.find_one({repet_key: repet_value}, {'_id': 0, repet_key: 1})
        return repet_data

    def run(self, item, repet_key, need_repet=False, repet_value=''):

        # asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.process(item, repet_key, need_repet, repet_value))

    def close(self):
        self.client.close()
        self.loop.close()


class MongoHandler2:
    '''非异步mongo'''

    def __init__(self, collection_name='default2', host=HOST, port=MONGO_PORT, user=MONGO_USER, pwd=MONGO_ADMIN_PWD,
                 db=DB_NAME):
        self.client = pymongo.MongoClient(host=host, port=int(port))
        self.db = self.client[db]

        self.db.authenticate(user, pwd)

        self.collection_name = collection_name  # for  logging
        self.collection = self.db[collection_name]

    def close(self):
        self.client.close()

    def find_one(self, repet_key, repet_value):
        result = self.collection.find_one({repet_key: repet_value}, {'_id': 0, repet_key: 1})
        # result = self.collection.find_one({'_values.{}'.format(repet_key): repet_value})
        return result

    def insert(self, item, repet_key='', need_repet=False, repet_value=''):

        if isinstance(item, Item):
            item_data = item.__dict__['_values']
        elif isinstance(item, dict):
            item_data = item
        else:
            try:
                item_data = json.loads(item)
            except:
                raise ('******************** item must dict ')

        if need_repet:
            if self.find_one(repet_key, repet_value):
                return logging.info('********************mongodb_{collection}==> repet :\n{item}'.format(
                    collection=self.collection_name, item=item_data))

        if self.collection.insert_one(item_data):
            logging.info('********************save to mongodb_{collection}==> success:\n{item}'.format( \
                collection=self.collection_name, item=item_data))
        else:
            raise (
            '********************save to mongodb_{collection}==> fail:\n{item}'.format(collection=self.collection_name,
                item=item_data))


if __name__ == '__main__':
    mh2 = MongoHandler2('jd_waterHot')
    # result = mh2.find_one('cid',12320831090)
    stu ={'cid': 12320831090,
 'content': '外观精美👍🤗🌹，显示屏幕大，使用起来放心安全！省电，安全，还可以实时预约功能，只需设置洗浴时间，就能使用热水。出水断电很安全，科技感也很足，可以手机APP操作！美的产品质量好，外观漂亮，大小合适，免费安装，感觉自己赚了！！有快递公司，服务态度超棒，约好时间后，售后马上来安装了！满分！',
 'creationTime': '2018-12-30 23:06:07',
 'images': ['//img30.360buyimg.com/n0/s128x96_jfs/t1/10383/11/7318/225328/5c28dedfE6b3ed064/dd0330219a91e7f0.jpg',
            '//img30.360buyimg.com/n0/s128x96_jfs/t1/12087/26/3719/221757/5c28dedfE4ef55d6f/84a550fcf7922b8d.jpg',
            '//img30.360buyimg.com/n0/s128x96_jfs/t1/8092/20/11251/150712/5c28dedfEc0b1fb45/950b3dc7b2d499d6.jpg',
            '//img30.360buyimg.com/n0/s128x96_jfs/t1/10183/24/7322/161199/5c28dedfE0854023b/808e2eae37db6a5c.jpg',
            '//img30.360buyimg.com/n0/s128x96_jfs/t1/22035/15/3610/146962/5c28dedfE68b6721d/ad02d507bf59bb55.jpg'],
 'productColor': '安全星铂金版A7S',
 'productSize': '60升',
 'score': 5}

    mh2.insert(stu)
    mh2.close()
    # print(result)
