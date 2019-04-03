#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '80022068'
__mtime__ = '2019/4/2'
# qq:2456056533

"""

# scrapy-splash + Nginx负载均衡测试: Nginx.logs

import requests


def lua_execute():
    from urllib.parse import quote
    lua = '''
        function main(splash)
        splash:go('http://news.163.com/latest/')   --需要爬取的url
        return splash:html()
        end
    '''
    execute_url = 'http://200.200.200.7:8049/execute?lua_source=' + quote(lua)
    resp = requests.get(execute_url)
    print(resp.text)



def di():
    url = 'https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=1046619896,177643554&fm=200&gp=0.jpg'
    pic = requests.get(url)
    with open('1.jpg','wb') as f:
        f.write(pic.content)

if __name__ == '__main__':
    # lua_execute()
    di()
