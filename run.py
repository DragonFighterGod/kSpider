#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/3/11'
# qq:2456056533


"""


def run_spider():
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    from kSpider.spiders.waterHot.jd import JDSpider, JDH5Spider
    from kSpider.spiders.waterHot.tb import TBSpider
    from kSpider.spiders.fruitsImg.fruits import FruitSpider
    process = CrawlerProcess(get_project_settings())
    process.crawl(FruitSpider)
    process.start()


def run_all():
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.project import get_project_settings

    from kSpider.spiders.waterHot.jd import JDSpider, JDH5Spider
    from kSpider.spiders.waterHot.tb import TBSpider
    from twisted.internet import reactor
    from scrapy.utils.log import configure_logging

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    runner = CrawlerRunner(get_project_settings())

    runner.crawl(JDSpider)
    runner.crawl(JDH5Spider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


if __name__ == '__main__':
    run_spider()
    # run_all()
