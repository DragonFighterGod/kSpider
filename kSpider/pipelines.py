# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re
# from kafka.producer import SimpleProducer
# from kafka.client import KafkaClient

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter

from kSpider.db.sqlBase import BaseModel, Session
from kSpider.db.mongoBase import MongoHandler, MongoHandler2
from kSpider.db.config import HOST, DB_NAME, MONGO_PORT, MONGO_ADMIN_PWD, MONGO_USER


def get_attr(spider, attr, df):
    if hasattr(spider, attr):
        spider_attr = getattr(spider, attr)
        _attr = spider_attr if spider_attr else df  # 属性= '' | None 取 df
    else:
        _attr = df
    return _attr


class CJsonItemPipline:
    '''
    自定义的json导出
    '''

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        filename = spider.name + '.txt'
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        with open(filename, 'a+', encoding='utf-8') as f:
            f.write(lines)

        return item

    def close_spider(self, spider):
        pass


class JsonItemExporterPipline:
    '''
    scrapy 内置的json 导出
    '''

    def open_spider(self, spider):
        filename = spider.name + '.json'

        self.file = open(filename, 'ab+')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)  # JsonItemExporter
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()  # 关闭
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)  # 写入item
        return item

        # @classmethod
        # def from_crawler(cls,crawler):
        #     s = cls(filename=crawler.settings.get(''))
        #     return s


class BaseSQLPipeline(object):
    def open_spider(self, spider):

        # BaseModel.drop_db()
        BaseModel.init_db()  # 建表

        self.session = Session()  # mysql_sesion

        self.need_repet = get_attr(spider, 'need_repet', df=False)

    def close_spider(self, spider):
        self.session.close()

    ### override
    def process_item(self, item, spider):
        # do something ,在子类实现item操作

        item = self.clear_item(item)
        return item

    def clear_item(self, item):
        '''item 去除\b\t等,ID to String,'''
        _item = {}
        for k, v in item.items():
            if v:
                _v = ''.join(str(v).split()).replace('👍', '').replace('🤗', '').replace('👌', '').replace('🌹','') \
                    .replace('👍', '').replace('🔥', '').replace('🌟', '').replace('⭐ ', '') \
                    .replace('\\n', '').replace('\\t','')\
                    .replace(' ', '').replace( '\\r','')
            else:
                _v = ''

            _item[k] = _v

        return _item


class BaseMongoPipeline(object):
    '''异步存mongodb
       这个类由于使用了mongo异步,所以只能同时一个爬虫调用这个Pipline,
       两个爬虫同时调用会出现: N1 关闭爬虫时会调用 loop.close(),导致N2没有 loop
       非得使用的话，注释 close_spider() 方法中的 self.mongo.close() 即可
    '''
    host = HOST
    port = MONGO_PORT
    user = MONGO_USER
    pwd = MONGO_ADMIN_PWD
    db = DB_NAME

    def open_spider(self, spider):
        collection_name = get_attr(spider, 'collection_name', df=spider.name)
        self.mongo = MongoHandler(collection_name=collection_name, host=self.host, port=self.port, user=self.user,
                                  pwd=self.pwd, db=self.db)

    def close_spider(self, spider):
        # self.mongo.close()
        pass

    def process_item(self, item, spider):
        need_repet = get_attr(spider, 'need_repet', df=False)
        repet_key = get_attr(spider, 'repet_key', df='url')

        if need_repet:
            self.mongo.run(item, repet_key, need_repet, repet_value=item[repet_key])  # mongo 查询去重
        else:
            self.mongo.run(item, repet_key, need_repet)

        return item


class BaseMongoPipeline2:
    '''非异步mongo'''
    host = HOST
    port = MONGO_PORT
    user = MONGO_USER
    pwd = MONGO_ADMIN_PWD

    db = DB_NAME

    def open_spider(self, spider):
        collection_name = get_attr(spider, 'collection_name', df=spider.name)
        self.mongo = MongoHandler2(collection_name=collection_name, host=self.host, port=self.port, user=self.user,
                                   pwd=self.pwd, db=self.db)

    def close_spider(self, spider):
        self.mongo.close()

    def process_item(self, item, spider):
        need_repet = get_attr(spider, 'need_repet', df=False)
        repet_key = get_attr(spider, 'repet_key', df='url')

        if need_repet:
            self.mongo.insert(item, repet_key, need_repet, item[repet_key])
        else:
            self.mongo.insert(item, repet_key, need_repet)

        return item


# class KafkaPopeline:
#     '''数据写入kafka内存'''
#
#     def __init__(self, producer, topic):
#         self.producer = producer
#         self.topic = topic
#         self.encoder = ScrapyJSONEncoder
#
#     def process_item(self, item, spider):
#         item = dict(item)
#         item['spider'] = spider.name
#         msg = self.encoder.encode(item)
#         self.producer.send_messages(self.topic, msg)
#         return item
#
#     @classmethod
#     def from_settings(cls, settings):
#         k_hosts = settings.get('Kafka_HOST', ['localhost:9092'])
#         topic = settings.get('Kafka_TOPIC', 'kafka_topic')
#         kafka_producer = SimpleProducer(KafkaClient(k_hosts))
#
#         return cls(kafka_producer, topic)
#

class ImgPipline(ImagesPipeline):
    '''图片下载'''

    def get_media_requests(self, item, info):
        dir_name = item['name']
        file_name = item['title']
        for url in item['img_urls']:
            if 'http' in url or 'https' in url:
                yield Request(url, meta={'dir_name': dir_name, 'file_name': file_name})
            else:
                url = 'http:' + url
                yield Request(url, meta={'dir_name': dir_name})  # 加上http

    def item_completed(self, results, item, info):
        img_paths = [x['path'] for ok, x in results if ok]

        if not img_paths:
            raise DropItem('no img')
        return item

    def file_path(self, request, response=None, info=None):

        dir_name = request.meta['dir_name']
        name = request.meta['file_name']
        dir_name = re.sub(r'[?\\*|“<>:/]', '', str(dir_name))  # 去除特殊字符
        name = re.sub(r'[?\\*|“<>:/]', '', str(name))
        filename = '{dir_name}/{name}.jpg'.format(dir_name=dir_name, name=name)
        return filename
