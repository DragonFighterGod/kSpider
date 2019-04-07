# -*- coding: utf-8 -*-
import scrapy

from kSpider.spiders.baseSpider.urlSpider import UrlSpider

tyurl_spider = 'tyc_url'


class TianyanchaSpider(UrlSpider):
    name = tyurl_spider

    redis_key = 'tyc'

    str_cookies = 'aliyungf_tc=AQAAAG9DKD/cYQcAOc97d2XzcQxh4E53; ssuid=9379214745; csrfToken=HgPWNEkZnaMHamjcrhsuT300; TYCID=d7e5fdf0590a11e9bf866d337a750b3d; undefined=d7e5fdf0590a11e9bf866d337a750b3d; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1554623873; _ga=GA1.2.638468641.1554623874; _gid=GA1.2.2012812491.1554623874; __insp_wid=677961980; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20v; __insp_targlpt=5aSp55y85p_lLeWVhuS4muWuieWFqOW3peWFt1%2FkvIHkuJrkv6Hmga%2Fmn6Xor6Jf5YWs5Y_45p_l6K_iX_W3peWVhuafpeivol%2FkvIHkuJrkv6HnlKjkv6Hmga%2Fns7vnu58%3D; __insp_norec_sess=true; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522zero2%2522%252C%2522integrity%2522%253A%252214%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522monitorUnreadCount%2522%253A%2522153%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzc4ODU3MzAyMCIsImlhdCI6MTU1NDYyMzg5NywiZXhwIjoxNTcwMTc1ODk3fQ.96qdjrNO_VIaZLjbTXxAIBvZVb4wOl4v0lCSfLI8qP4yAhkv4VuzLAVeuDaixAx2AU4Cy-xEQFVsXvw6gmigtw%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217788573020%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzc4ODU3MzAyMCIsImlhdCI6MTU1NDYyMzg5NywiZXhwIjoxNTcwMTc1ODk3fQ.96qdjrNO_VIaZLjbTXxAIBvZVb4wOl4v0lCSfLI8qP4yAhkv4VuzLAVeuDaixAx2AU4Cy-xEQFVsXvw6gmigtw; _gat_gtag_UA_123487620_1=1; RTYCID=9885f4ef7c1c4858b8ee6c4a06546ae1; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1554624059; __insp_slim=1554624058864; CT_TYCID=0411fa07bbe44682aed396e490191ca3'

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
