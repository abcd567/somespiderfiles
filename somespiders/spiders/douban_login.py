# -*- coding: utf-8 -*-
import json
import time
import pickle
import os

import scrapy
from scrapy import FormRequest, Request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pyautogui


class DoubanLoginSpider(scrapy.Spider):
    name = 'douban_login'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "COOKIES_ENABLED": True,
        "COOKIES_DUBUG": True,
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    }

    # def start_requests(self):
    #     form_data = {
    #         'ck': '',
    #         'name': '15986744115',
    #         'password': 'slzkszkbjz123',
    #         'remember': 'false',
    #         'ticket': ''
    #     }
    #
    #     yield FormRequest(
    #         url='https://accounts.douban.com/j/mobile/login/basic',
    #         headers=self.headers,
    #         method='POST',
    #         formdata=form_data,
    #         callback=self.parse
    #     )
    #
    #
    # def parse(self, response):
    #     data = response.body.decode('utf8')
    #     print(data)
    #     # 过于频繁登陆会出现验证码
    #     if data['status'] == 'failed':
    #         if data['message'] == 'captcha_required':
    #             cimg_url = data['captcha_image_url']
    #             print("出现登陆验证码:" + cimg_url)
    #             print("使用selenium会用滑块验证码")
    #     pass

    # 在豆瓣首页登陆可以免去验证码，采用selenium模拟登陆，获取cookies
    def start_requests(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        browser = webdriver.Chrome(executable_path='I:\\谷歌下载\\chromedriver_win32\\chromedriver.exe', options=option)

        browser.get("http://douban.com/")
        # 窗口最大化
        try:
            browser.maximize_window()
        except Exception as e:
            print(e)

        try:
            # 若出现没有登陆页面
            if WebDriverWait(browser, 20).until(lambda x: x.find_element_by_xpath('//div[@id="anony-nav"]')):
                # 选择密码登陆，元素找不到，选择坐标
                # browser.find_element_by_xpath('//ul[@class="tab-start"]/li[@class="account-tab-account"]').click()
                # 关掉开发者模式提示
                pyautogui.click(x=1818, y=83, duration=1.5)
                time.sleep(3)
                # 点击密码登陆
                pyautogui.click(1350, 200, duration=1.5)
                time.sleep(3)
                # 点击账号输入框
                pyautogui.click(1250, 270, duration=1.5)
                time.sleep(1)
                # 输入账号
                pyautogui.typewrite(message='159****4115', interval=0.5)
                time.sleep(1)
                # 点击密码输入框
                pyautogui.click(1250, 320, duration=1.5)
                time.sleep(1)
                # 输入密码
                pyautogui.typewrite(message='slzk*****', interval=0.5)
                time.sleep(1)
                # 点击登陆按钮
                pyautogui.click(1250, 370, duration=1.5)
                time.sleep(10)
                """搞定"""
                # browser.find_element_by_xpath('//input[@id="username"]').send_keys('159****4115')
                # time.sleep(1)
                # browser.find_element_by_xpath('//input[@id="password"]').send_keys('slzk*****')
                # time.sleep(1)
                # browser.find_element_by_xpath('//a[@class="btn btn-account"]').click()
        except Exception as e:
            print(type(e), ':', e)

        # 获取cookie 并保存
        cookies = browser.get_cookies()
        for cookie in cookies:
            # 写入文件
            # 此处大家修改一下自己文件的所在路径
            f = open(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\cookies\\douban\\' + cookie['name'] + '.douban', 'wb'
            )
            pickle.dump(cookie, f)
        f.close()
        # 包装我要的cookies
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie["name"]] = cookie["value"]
        # dont_filter为True ,访问过的url不会过滤掉
        yield scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict, headers=self.headers)

    def parse(self, response):
        print(response.text)
        pass