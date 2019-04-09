# -*- coding: utf-8 -*-
import scrapy

from kSpider.spiders.baseSpider.urlSpider import UrlSpider

tyurl_spider = 'tyc_url'


class TianyanchaSpider(UrlSpider):
    name = tyurl_spider

    redis_key = 'tyc'

    str_cookies = '登录后的cookies,===> b38ck2icdtlutt94; UM_distinctid=169f6fad96c33d'

    base_url = 'https://www.tianyancha.com/search/p{page}?key={key}'


    custom_settings = UrlSpider.custom_settings.copy()
    custom_settings['DOWNLOAD_DELAY'] = 20

    def fuzzy_search(self):
        '''
        模糊搜索
        :return: 
        '''

        search_keys = ['家具']
        self.cookies = self.string_to_dict(self.str_cookies)
        end_page = 5
        for i in search_keys:
            for j in range(1, end_page):  # 非会员(登不登录都只有5页,但是不登录容易被重定向到登录页)
                yield scrapy.Request(url=self.base_url.format(page=j, key=i), callback=self.url_parse,
                                     cookies=self.cookies, dont_filter=True)

    def key_search(self):
        '''
        关键字搜索
        :return: 
        '''
        from kSpider.spiders.qichacha.other.fullname import get_name
        search_keys = get_name()
        self.cookies = self.string_to_dict(self.str_cookies)
        # for i in range(0,4):
        for i in range(0, len(search_keys)):
            yield scrapy.Request(url='https://www.tianyancha.com/search?key={}'.format(search_keys[i]),
                                 callback=self.url_parse, cookies=self.cookies, dont_filter=True)

    def start_requests(self):
        # self.fuzzy_search()
        # self.key_search()
        for request in self.fuzzy_search():
            yield request

    def url_parse(self, response):

        # lpush tyc 'https://www.tianyancha.com/company/3179817455'
        # lpush tyc 'https://www.tianyancha.com/company/2366253319'
        for i in response.xpath('//div[@class="search-item sv-search-company"]/div'):
            url = i.xpath('div[3]/div/a/@href').extract_first()
            self.add_url(url)



if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(TianyanchaSpider)
    process.start()
