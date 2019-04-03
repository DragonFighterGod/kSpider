#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'stringk'
__mtime__ = '2019/2/25'
# qq:2456056533

"""

import platform
import time
from threading import Thread, BoundedSemaphore

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from kSpider.settings import CHROME_DRIVER

proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

proxyUser = "H4X82BC0EL1ZS69D"
proxyPass = "85B833C15C8950BA"


def get_browser(executable_path=CHROME_DRIVER):
    timeout = 30

    PROXY = create_proxy_auth(proxy_host=proxyHost, proxy_port=proxyPort, proxy_username=proxyUser,
                              proxy_password=proxyPass)

    if PROXY:
        desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
        desired_capabilities['proxy'] = {"httpProxy": PROXY, "ftpProxy": PROXY, "sslProxy": PROXY, "noProxy": None,
                                         "proxyType": "MANUAL", "class": "org.openqa.selenium.Proxy",
                                         "autodetect": False}
    else:
        desired_capabilities = None

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])

    # proxy_auth_plugin_path = create_proxy_auth_extension(proxy_host=proxyHost, proxy_port=proxyPort,proxy_username=proxyUser, proxy_password=proxyPass)
    # options.add_extension(proxy_auth_plugin_path)


    if platform.system() == 'Windows':
        browser = webdriver.Chrome(executable_path=executable_path, chrome_options=options,
                                   desired_capabilities=desired_capabilities)
    else:
        options.add_argument('--no-sandbox')
        # options.add_argument('--disable-setuid-sandbox')
        browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options,
                                   desired_capabilities=desired_capabilities)

    browser.maximize_window()
    browser.set_page_load_timeout(timeout)
    browser.implicitly_wait(timeout)
    wait = WebDriverWait(browser, timeout)

    return browser, wait


def create_proxy_auth(proxy_host, proxy_port, proxy_username, proxy_password):
    proxies = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {"host": proxy_host, "port": proxy_port,
                                                              "user": proxy_username, "pass": proxy_password, }

    return proxies


# def create_proxy_auth_extension(proxy_host, proxy_port, proxy_username, proxy_password, scheme='http',
#                                 plugin_path=None):
#     '''只适用于有头浏览器'''
#
#     if plugin_path is None:
#         if platform.system() == 'Windows':
#             plugin_path = r'D:/{}_{}@http-dyn.abuyun.com_9020.zip'.format(proxy_username, proxy_password)
#         else:
#             plugin_path = '/home/stringk/{}_{}@http-dyn.abuyun.com_9020.zip'.format(proxy_username, proxy_password)
#
#     manifest_json = """
#         {
#             "version": "1.0.0",
#             "manifest_version": 2,
#             "name": "Abuyun Proxy",
#             "permissions": [
#                 "proxy",
#                 "tabs",
#                 "unlimitedStorage",
#                 "storage",
#                 "<all_urls>",
#                 "webRequest",
#                 "webRequestBlocking"
#             ],
#             "background": {
#                 "scripts": ["background.js"]
#             },
#             "minimum_chrome_version":"70.0.3"
#         }
#         """
#
#     background_js = string.Template("""
#             var config = {
#                 mode: "fixed_servers",
#                 rules: {
#                     singleProxy: {
#                         scheme: "${scheme}",
#                         host: "${host}",
#                         port: parseInt(${port})
#                     },
#                     bypassList: ["foobar.com"]
#                 }
#               };
#
#             chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
#
#             function callbackFn(details) {
#                 return {
#                     authCredentials: {
#                         username: "${username}",
#                         password: "${password}"
#                     }
#                 };
#             }
#
#             chrome.webRequest.onAuthRequired.addListener(
#                 callbackFn,
#                 {urls: ["<all_urls>"]},
#                 ['blocking']
#             );
#             """).substitute(host=proxy_host, port=proxy_port, username=proxy_username, password=proxy_password,
#                             scheme=scheme, )
#
#     with zipfile.ZipFile(plugin_path, 'w') as zp:
#         zp.writestr("manifest.json", manifest_json)
#         zp.writestr("background.js", background_js)
#
#     return plugin_path


def request_proxy_t():
    import requests
    proxy = create_proxy_auth(proxy_host=proxyHost, proxy_port=proxyPort, proxy_username=proxyUser,
                              proxy_password=proxyPass)
    proxies = {'http': proxy, 'https': proxy}
    resp = requests.get('https://www.baidu.com/', proxies=proxies)
    print(resp.status_code)


class Driver:
    def __init__(self, executable_path=r'D:/develop/seleniumDrivers/chromedriver.exe'):
        self.driver, self.wait = get_browser(executable_path)
        self.action = ActionChains(self.driver)

    def js_execute(self, js):
        self.driver.execute_script(js)

    def find_xpath(self, xpath):
        element = self.wait.until(lambda d: d.find_element_by_xpath(xpath))
        return element

    def find_id(self, id):
        element = self.wait.until(lambda d: d.find_element_by_id(id))
        return element

    def find_class_name(self, class_name):
        element = self.wait.until(lambda d: d.find_elements_by_class_name(class_name))
        return element

    def action_click(self, element):
        self.action.click(element).perform()

    @staticmethod
    def is_pixel_equal(bg_image, fullbg_image, x, y):
        """
        判断像素是否相同
        :param bg_image: (Image)残缺图
        :param fullbg_image: (Image)完整图
        :param x: (Int)位置x
        :param y: (Int)位置y
        :return: (Boolean)像素是否相同
        """
        bg_pixel = bg_image.load()[x, y]
        fullbg_pixel = fullbg_image.load()[x, y]
        threshold = 60

        if (abs(bg_pixel[0] - fullbg_pixel[0] < threshold) and abs(bg_pixel[1] - fullbg_pixel[1] < threshold) and abs(
                        bg_pixel[2] - fullbg_pixel[2] < threshold)):
            return True

        else:
            return False

    def get_distance(self, bg_image, fullbg_image, slider_distance):
        '''
        滑块移动距离
        :param bg_image: (Image)残缺图
        :param fullbg_image: (Image)完整图片
        :param slider_distance:  滑块的初始位置
        :return: (Int)滑块滑动距离
        '''

        for i in range(slider_distance, fullbg_image.size[0]):
            for j in range(fullbg_image.size[1]):
                if not self.is_pixel_equal(fullbg_image, bg_image, i, j):
                    return i

    @staticmethod
    def get_trace(distance):
        '''
        构造滑动轨迹
        :param distance: (Int)缺口离滑块的距离
        :return: (List)移动轨迹
        '''
        trace = []
        faster_distance = distance * (4 / 5)
        start, v0, t = 0, 0, 0.2
        while start < distance:
            if start < faster_distance:
                a = 6
            else:
                a = -3
            move = v0 * t + 1 / 2 * a * t * t
            v = v0 + a * t
            v0 = v
            start += move
            trace.append(round(move))
        return trace

    def move_to_gap(self, slider, mv_distance, offset=0):
        '''
        滑动滑块
        :param slider:  滑块元素
        :param mv_distance:  滑动距离
        :param offset:  滑动距离偏移量调整
        :return:
        '''
        trace = self.get_trace(mv_distance - offset)
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in trace:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

    @staticmethod
    def thread_run(class_name, cates, sem=3):
        semlock = BoundedSemaphore(sem)  # threading.BoundedSemaphore()
        for cate in cates:
            semlock.acquire()
            if isinstance(class_name, object):
                obj = class_name()
                if hasattr(obj, 'start'):
                    thread = Thread(target=obj.start, args=(cate,))
                    # threads.append(thread)
                    thread.start()
                else:
                    raise ('*******obj has no start func')


if __name__ == '__main__':
    driver, wait = get_browser()
    driver.get('https://www.baidu.com/')
    time.sleep(5)
    driver.quit()
    # request_proxy_()
