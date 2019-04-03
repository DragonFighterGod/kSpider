#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2019/2/22'
# qq:2456056533

"""
import json
import logging
from contextlib import contextmanager
from scrapy import Item

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from kSpider.db.config import HOST, DB_NAME, MYSQL_ROOT_PWD, MYSQL_USER, MYSQL_PORT

Base = declarative_base()

engine = create_engine(
    'mysql+pymysql://{user}:{pwd}@{host}:{port}/{db_name}?charset=utf8'.format(user=MYSQL_USER, pwd=MYSQL_ROOT_PWD,
                                                                               host=HOST, port=MYSQL_PORT,
                                                                               db_name=DB_NAME), echo=False)


# engine = create_engine(
#     'mysql+pymysql://{user}:{pwd}@{host}:{port}/{db_name}?autocommit=true'\
#         .format(user=MYSQL_USER,pwd=MYSQL_ROOT_PWD,host=HOST,port=MYSQL_PORT,db_name=DB_NAME),echo=False)
#



def create_newtable(engine):
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        raise ('--------------create_all err：创建表失败--------------')


def get_sqlsession(engine):
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except Exception as e:
        raise ('--------------engine err: 数据库连接错误--------------')


class BaseModel(Base):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)

    @staticmethod
    def set_attrs(attrs_datas, model_obj):
        if not isinstance(attrs_datas, dict):
            try:
                attrs_datas = json.loads(attrs_datas)
            except Exception as e:
                raise e

        for k, v in attrs_datas.items():
            if hasattr(model_obj, k) and k != 'id':
                setattr(model_obj, k, str(v))

    @classmethod
    def save_mode(cls, session, model, item=None):
        if item:
            if isinstance(item, Item):
                item_data = item.__dict__['_values']

            elif isinstance(item, dict):
                item_data = item
            else:
                try:
                    item_data = json.loads(item)
                except:
                    raise ('******************** item must dict ')

            cls.set_attrs(item_data, model)

            try:
                session.add(model)
                session.commit()
                logging.info('**********************save to mysql ==> successful:\n%s' % item_data)
            except Exception as e:
                logging.info('**********************save to mysql ==> fail:\n{err}'.format(err=e))
                session.rollback()

    @staticmethod
    @contextmanager
    def auto_commit(session):
        try:
            yield
            session.commit()
        except Exception as e:
            session.rollback()

    @staticmethod
    def db_distinct(session, dbmodel, item, keywords, need_repet=False):
        '''
        Db 通过url去重,可选
        '''

        if not need_repet: return item

        try:
            result = session.query(dbmodel.id).filter_by(url=keywords).first()
        except Exception as e:
            session.rollback()
            result = 1

        if result:
            logging.info('**********************save to mysql ==> repet:\n%s' % item)

        else:
            return item


'''
CREATE DATABASE IF NOT EXISTS spider default charset utf8 COLLATE utf8_general_ci;
flush privileges;

'''