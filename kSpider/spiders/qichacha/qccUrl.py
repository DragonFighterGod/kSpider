# -*- coding: utf-8 -*-
import scrapy

from kSpider.spiders.baseSpider.urlSpider import UrlSpider

qiurl_spider = 'qcc_url'


class QccurlSpider(UrlSpider):
    name = qiurl_spider
    redis_key = 'qcc'

    str_cookies = '登录后的cookies,===> b38ck2icdtlutt94; UM_distinctid=169f6fad96c33d'

    allowed_domains = ['qichacha.com']
    base_url = 'https://www.qichacha.com'

    custom_settings = UrlSpider.custom_settings.copy()
    custom_settings['DOWNLOAD_DELAY'] = 20



    def fuzzy_search(self):
        '''
        模糊搜索
        :return:
        '''

        search_keys = ['家具', ]
        page_num = 2  # 11                   # 普通会员限制10页
        self.cookies = self.string_to_dict(self.str_cookies)
        for i in search_keys:
            for j in range(1, page_num):
                url = self.base_url + '/search?key=' + i + '&p={}&'.format(j)
                yield scrapy.Request(url, callback=self.url_parse, cookies=self.cookies)

    def key_search(self):
        '''
        关键字搜索
        :return:
        '''
        from kSpider.spiders.qichacha.other.fullname import get_name
        search_keys = get_name()
        self.cookies = self.string_to_dict(self.str_cookies)
        # for i in range(0,3):
        for i in range(0, len(search_keys)):
            yield scrapy.Request(url=self.base_url + '/search?key={}'.format(search_keys[i]), callback=self.url_parse,
                                 cookies=self.cookies)

    def start_requests(self):
        # self.fuzzy_search()
        # self.key_search()
        for request in self.fuzzy_search():
            yield request

    def url_parse(self, response):

        # if 'www.qichacha.com/index_verify?' in response.text:  # 滑块认证-pass
        #     auth_url = response.text.split("'")[1]            # https://www.qichacha.com/index_verify?type=companysearch&back=/search?key=%E8%BD%AF%E8%A3%85&p=1&
        #     yield scrapy.Request(auth_url,callback=self.url_parse,cookies=self.cookies)

        trs = response.xpath('//section[@id="searchlist"]/table/tbody/tr')
        if not trs:
            trs = response.xpath('//section[@id="searchlist"]/table/tr')
        for tr in trs:
            url = tr.xpath('td[3]/a/@href').extract_first()
            if not url:
                url = tr.xpath('td[2]/a/@href').extract_first()

            self.add_url(self.base_url+url)


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    # process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process = CrawlerProcess(get_project_settings())
    process.crawl(QccurlSpider)
    process.start()
