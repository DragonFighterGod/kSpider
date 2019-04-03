#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/3/18'
# qq:2456056533

"""

import scrapy

from scrapy_splash import SplashRequest

class SplashSpider(scrapy.Spider):
    name = "splash"

    allowed_domains = []
    start_urls = []
    base_url = ''
    cookies = {}


    # 可选参数：
    collection_name = ''  # 默认collection_name = spider.name
    need_repet = False  # 默认不查询去重
    repet_key = ''  # 查询key


    # splash设置
    DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
    HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
    custom_settings = {'DOWNLOAD_DELAY': 3, 'CONCURRENT_REQUESTS': 6, 'CONCURRENT_REQUESTS_PER_DOMAIN': 6,
                       'SPIDER_MIDDLEWARES': {'scrapy_splash.SplashDeduplicateArgsMiddleware': 100, },
                       'DOWNLOADER_MIDDLEWARES': {'scrapy_splash.SplashCookiesMiddleware': 723,
                                                  'scrapy_splash.SplashMiddleware': 725,
                                                  'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,},
                       'ITEM_PIPELINES': {'kSpider.pipelines.BaseMongoPipeline2': 300, }}

    def start_requests(self):
        for url in self.start_urls:
            # yield SplashRequest(url, endpoint="execute",callback=self.parse_item,args={'wait':3,'lua_source':SplashApi.lua_scroll,'proxy':'http://http://proxy_ip:proxy_port'})
            yield SplashRequest(url, endpoint="execute",callback=self.parse_item, args={'wait': 3, 'lua_source': SplashApi.lua_scroll_2})

    def parse_item(self, response):
        pass



class SplashApi:
    lua_proxy = '''
    function main(splash)
        splash:on_request(function(request)
        request:set_proxy{
	        host = "127.0.0.1",
	        port = 8000,
	    }
		end)
        splash:go(splash.args.url)
        return splash:html()
    end
    
    '''
    lua_scroll = '''
    function main(splash)
        splash:go(splash.args.url)
        splash:wait(3)
        splash:runjs("document.getElementsByClassname('page')[0].scrollIntoView(true)")
        splash:wait(2)
        return splash:html()
    end
    '''

    lua_scroll_2 ='''
    function main(splash, args)
        -- splash:set_viewport_size(1028, 10000)
        splash:go(args.url)
        local scroll_to = splash:jsfunc("window.scrollTo")
        scroll_to(0, 2000)
        splash:wait(5)
        return splash:html()
    end
    '''

    lua_scroll_3 ='''
    function main(splash, args)
        -- splash:set_viewport_size(1028, 10000)
        splash:go(args.url)
        splash.scroll_position={0,2000}
        splash:wait(5)
        return {png=splash:png()}
    end
    '''


    lua_click='''
    function main(splash)
        splash:go(splash.args.url)
        splash:wait(3)
        splash:runjs("document.getElementsByClassname('btn').onclick=function(){ }") 
        splash:wait(2)
        return splash:html()
    end
    
    '''

    lua_click2 = '''
     function main(splash)
    	splash:go(splash.args.url) 
    	splash:wait(0.5) 
    	local title = splash:evaljs('document.getElementById("")') --执行js代码并返回值
    	return {title = title}
    	-- return splash:html()
    end
    '''



if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(SplashSpider)
    process.start()
