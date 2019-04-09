# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import platform
from logging import getLogger
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from kSpider.agents2 import AGENTS_ALL


class UserAgentDownloaderMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS_ALL)
        request.headers['User-Agent'] = agent

        # request.meta['splash']['args']['proxy'] = proxyServer
        # request.headers["Proxy-Authorization"] = proxyAuth

    def process_exception(self, request, exception, spider):
        with open('{}err.txt'.format(spider.name), 'a+')as f:
            f.write(request.url + '\n')

        spider.logger.info(exception)


class SeleniumDownloaderMiddleware:
    def __init__(self, executable_path=None):
        self.logger = getLogger(__name__)
        self.timeout = 20

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # --ingor

        if platform.system() == 'Windows':
            self.browser = webdriver.Chrome(executable_path=executable_path, chrome_options=options)
        else:
            options.add_argument('--no-sandbox')
            self.browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)

        self.browser.maximize_window()
        self.browser.set_page_load_timeout(self.timeout)
        self.browser.implicitly_wait(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(executable_path=crawler.settings.get('CHROME_DRIVER'))
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    # def close_spider(self,spider):
    #     self.browser.quite()

    def spider_closed(self, spider):
        self.browser.delete_all_cookies()
        self.browser.quit()

    # override
    def do_something(self):
        #
        # do something
        # js_down = 'var q=document.documentElement.scrollTop=10000'
        # self.browser.execute_script(js_down)

        pass


    def process_request(self, request, spider):
        self.logger.info('Chrome is Starting')
        try:
            self.browser.get(request.url)

            self.do_something()

            page_source = self.browser.page_source
            self.browser.delete_all_cookies()
            return HtmlResponse(url=request.url, body=page_source, request=request, encoding='utf-8', status=200)

        except:
            with open('{}err.txt'.format(spider.name), 'a+')as f:
                f.write(request.url + '\n')

            self.logger.info('超时异常url:%s' % request.url)




class ExecJsDownloaderMiddleware:
    def process_request(self, request, spider):
        agent = random.choice(AGENTS_ALL)
        request.headers['User-Agent'] = agent

    def process_response(self, request, response, spider):
        pass

        return response

# class KspiderSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
#
#
# class KspiderDownloaderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.
#
#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None
#
#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.
#
#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.
#
#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
