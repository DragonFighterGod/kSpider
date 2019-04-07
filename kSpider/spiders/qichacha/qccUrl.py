# -*- coding: utf-8 -*-
import scrapy

from kSpider.spiders.baseSpider.urlSpider import UrlSpider

qiurl_spider = 'qcc_url'


class QccurlSpider(UrlSpider):
    name = qiurl_spider
    redis_key = 'qcc'

    str_cookies = 'QCCSESSID=l113177mm2b38ck2icdtlutt94; UM_distinctid=169f6fad96c33d-0b5824b39c3d8e-e323069-1fa400-169f6fad96dc9; CNZZDATA1254842228=2123228801-1554622448-https%253A%252F%252Fwww.baidu.com%252F%7C1554622448; zg_did=%7B%22did%22%3A%20%22169f6fada381f7-0090f0bbf82a26-e323069-1fa400-169f6fada39527%22%7D; hasShow=1; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1554626829; _uab_collina=155462682916145363826508; acw_tc=7793462115546268295363829eaf18fd8cfe0ef4d93dde9a6230cc7077; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1554627148; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201554626828861%2C%22updated%22%3A%201554627150522%2C%22info%22%3A%201554626828868%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%22265d30ecc365058984801223ceaf0330%22%7D'

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
