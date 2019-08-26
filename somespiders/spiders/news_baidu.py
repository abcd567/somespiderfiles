# -*- coding: utf-8 -*-
import re
import time
import json

import scrapy

from somespiders.items import BaiduNewsItem



class NewsBaiduSpider(scrapy.Spider):
    name = 'news_baidu'
    allowed_domains = ['news.baidu.com']
    start_urls = ['http://news.baidu.com/widget?id=civilnews',
                  'http://news.baidu.com/widget?id=DiscoveryNews',
                  'http://news.baidu.com/widget?id=EnterNews',
                  'http://news.baidu.com/widget?id=FinanceNews',
                  'http://news.baidu.com/widget?id=HealthNews',
                  'http://news.baidu.com/widget?id=InternationalNews',
                  'http://news.baidu.com/widget?id=InternetNews',
                  'http://news.baidu.com/widget?id=LadyNews',
                  'http://news.baidu.com/widget?id=LocalNews&ajax=json&t={0}'.format(int(time.time()*1000)),
                  'http://news.baidu.com/widget?id=MilitaryNews&ajax=json',
                  'http://news.baidu.com/widget?id=PicWall&ajax=json',
                  'http://news.baidu.com/widget?id=SportNews&ajax=json',
                  'http://news.baidu.com/widget?id=TechNews&ajax=json',
                  ]

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "ITEM_PIPELINES": {
            'somespiders.pipelines.MySQLPileline': 300,
        }
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    }

    def parse(self, response):
        pass

    def start_requests(self):
        pat = pat = re.compile('http://news.baidu.com/widget\?id=(.*?)(&aj.*|$)')
        for url in self.start_urls:
            widget_id = pat.findall(url)[0][0]
            handle_name = 'handle_' + widget_id.lower()
            yield scrapy.Request(url=url, dont_filter=True, headers=self.headers,
                                 callback=self.__getattribute__(handle_name))

    def handle_civilnews(self, response):
        # 国内China板块 共12条
        focuslistnews_title = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/text()').extract()
        focuslistnews_link = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/@href').extract()
        for i in range(0, len(focuslistnews_title)):
            item = BaiduNewsItem()
            item['title'] = focuslistnews_title[i]
            item['news_type'] = 'civilnews'
            item['has_img'] = 0
            item['news_link'] = focuslistnews_link[i]
            item['img_url'] = ''
            yield item

        # 国内图片板块 共3条
        # mask部分 1条
        imgarea_mask_title = response.xpath('//div[@class="image-mask-item"]/a[@class="item-title"]/@title').extract()
        imgarea_mask_link = response.xpath('//div[@class="image-mask-item"]/a[@class="item-image"]/@href').extract()
        imgarea_mask_img = response.xpath('//div[@class="image-mask-item"]/a[@class="item-image"]/img/@src').extract()
        for i in range(0, len(imgarea_mask_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_mask_title[i]
            item['news_type'] = 'civilnews'
            item['has_img'] = 1
            item['news_link'] = imgarea_mask_link[i]
            item['img_url'] = imgarea_mask_img[i]
            yield item

        # 其余部分 2条
        imgarea_title = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        imgarea_link = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        imgarea_img = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(imgarea_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_title[i]
            item['news_type'] = 'civilnews'
            item['has_img'] = 1
            item['news_link'] = imgarea_link[i]
            item['img_url'] = imgarea_img[i]
            yield item

        # 图文资讯板块 2条
        imglist_title = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        imglist_link = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        imglist_img = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(imglist_title)):
            item = BaiduNewsItem()
            item['title'] = imglist_title[i]
            item['news_type'] = 'civilnews'
            item['has_img'] = 1
            item['news_link'] = imglist_link[i]
            item['img_url'] = imglist_img[i]
            yield item


        # 热门点击板块 5条
        hotclick_title = response.xpath(
            '//ol[@class="olist "]/li/a/@title'
        ).extract()
        hotclick_link = response.xpath(
            '//ol[@class="olist "]/li/a/@href'
        ).extract()
        for i in range(0, len(hotclick_title)):
            item = BaiduNewsItem()
            item['title'] = hotclick_title[i]
            item['news_type'] = 'civilnews'
            item['has_img'] = 0
            item['news_link'] = hotclick_link[i]
            item['img_url'] = ''
            yield item

        time.sleep(60)
        yield scrapy.Request(url=response.url, dont_filter=True, headers=self.headers,
                             callback=self.handle_civilnews)

    def handle_discoverynews(self, response):
        # 探索板块 focus 12条
        focuslistnews_title = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/text()').extract()
        focuslistnews_link = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/@href').extract()
        for i in range(0, len(focuslistnews_title)):
            item = BaiduNewsItem()
            item['title'] = focuslistnews_title[i]
            item['news_type'] = 'discoverynews'
            item['has_img'] = 0
            item['news_link'] = focuslistnews_link[i]
            item['img_url'] = ''
            yield item

        # 探索图片板块 共3条
        # mask部分 1条
        imgarea_mask_title = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-title"]/@title').extract()
        imgarea_mask_link = response.xpath('//div[@class="image-mask-item"]/a[@class="item-image"]/@href').extract()
        imgarea_mask_img = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-image"]/img/@src').extract()
        for i in range(0, len(imgarea_mask_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_mask_title[i]
            item['news_type'] = 'discoverynews'
            item['has_img'] = 1
            item['news_link'] = imgarea_mask_link[i]
            item['img_url'] = imgarea_mask_img[i]
            yield item

        # 其余部分 2条
        imgarea_title = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        imgarea_link = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        imgarea_img = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(imgarea_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_title[i]
            item['news_type'] = 'discoverynews'
            item['has_img'] = 1
            item['news_link'] = imgarea_link[i]
            item['img_url'] = imgarea_img[i]
            yield item

        # 探索话题板块 置顶2条有封面
        topic_top_title = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        topic_top_link = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        topic_top_img = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(topic_top_title)):
            item = BaiduNewsItem()
            item['title'] = topic_top_title[i]
            item['news_type'] = 'discoverynews'
            item['has_img'] = 1
            item['news_link'] = topic_top_link[i]
            item['img_url'] = topic_top_img[i]
            yield item

        # 探索话题板块 后7条无封面
        topic_title = response.xpath(
            '//ul[@class="ulist "]/li/a/text()'
        ).extract()
        topic_link = response.xpath(
            '//ul[@class="ulist "]/li/a/@href'
        ).extract()
        for i in range(0, len(topic_title)):
            item = BaiduNewsItem()
            item['title'] = topic_title[i]
            item['news_type'] = 'discoverynews'
            item['has_img'] = 0
            item['news_link'] = topic_link[i]
            item['img_url'] = ''
            yield item

        # time.sleep(60)
        # yield scrapy.Request(url=response.url, dont_filter=True, headers=self.headers,
        #                      callback=self.handle_discoverynews)

    def handle_enternews(self, response):
        # 娱乐板块 focus共12条
        focuslistnews_title = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/text()').extract()
        focuslistnews_link = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/@href').extract()
        for i in range(0, len(focuslistnews_title)):
            item = BaiduNewsItem()
            item['title'] = focuslistnews_title[i]
            item['news_type'] = 'enternews'
            item['has_img'] = 0
            item['news_link'] = focuslistnews_link[i]
            item['img_url'] = ''
            yield item

        # 娱乐图片板块 共3条
        # mask部分 1条
        imgarea_mask_title = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-title"]/@title').extract()
        imgarea_mask_link = response.xpath('//div[@class="image-mask-item"]/a[@class="item-image"]/@href').extract()
        imgarea_mask_img = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-image"]/img/@src').extract()
        for i in range(0, len(imgarea_mask_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_mask_title[i]
            item['news_type'] = 'enternews'
            item['has_img'] = 1
            item['news_link'] = imgarea_mask_link[i]
            item['img_url'] = imgarea_mask_img[i]
            yield item

        # 其余部分 2条
        imgarea_title = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        imgarea_link = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        imgarea_img = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(imgarea_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_title[i]
            item['news_type'] = 'enternews'
            item['has_img'] = 1
            item['news_link'] = imgarea_link[i]
            item['img_url'] = imgarea_img[i]
            yield item

        # 明星板块 7条有封面
        topic_top_title = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        topic_top_link = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        topic_top_img = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(topic_top_title)):
            item = BaiduNewsItem()
            item['title'] = topic_top_title[i]
            item['news_type'] = 'enternews'
            item['has_img'] = 1
            item['news_link'] = topic_top_link[i]
            item['img_url'] = topic_top_img[i]
            yield item

        # 探索话题板块 7条无封面
        topic_title = response.xpath(
            '//ul[@class="ulist "]/li/a/text()'
        ).extract()
        topic_link = response.xpath(
            '//ul[@class="ulist "]/li/a/@href'
        ).extract()
        for i in range(0, len(topic_title)):
            item = BaiduNewsItem()
            item['title'] = topic_title[i]
            item['news_type'] = 'enternews'
            item['has_img'] = 0
            item['news_link'] = topic_link[i]
            item['img_url'] = ''
            yield item

        # time.sleep(60)
        # yield scrapy.Request(url=response.url, dont_filter=True, headers=self.headers,
        #                      callback=self.handle_enternews)

    def handle_financenews(self, response):
        # 财经板块 focus共12条
        focuslistnews_title = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/text()').extract()
        focuslistnews_link = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/@href').extract()
        for i in range(0, len(focuslistnews_title)):
            item = BaiduNewsItem()
            item['title'] = focuslistnews_title[i]
            item['news_type'] = 'financenews'
            item['has_img'] = 0
            item['news_link'] = focuslistnews_link[i]
            item['img_url'] = ''
            yield item

        # 财经图片板块 共3条
        # mask部分 1条
        imgarea_mask_title = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-title"]/@title').extract()
        imgarea_mask_link = response.xpath('//div[@class="image-mask-item"]/a[@class="item-image"]/@href').extract()
        imgarea_mask_img = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-image"]/img/@src').extract()
        for i in range(0, len(imgarea_mask_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_mask_title[i]
            item['news_type'] = 'financenews'
            item['has_img'] = 1
            item['news_link'] = imgarea_mask_link[i]
            item['img_url'] = imgarea_mask_img[i]
            yield item

        # 其余部分 2条
        imgarea_title = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        imgarea_link = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        imgarea_img = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(imgarea_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_title[i]
            item['news_type'] = 'financenews'
            item['has_img'] = 1
            item['news_link'] = imgarea_link[i]
            item['img_url'] = imgarea_img[i]
            yield item

        # 股指期货数据——来源：网易财经
        item = BaiduNewsItem()
        item['title'] = '股指期货数据'
        item['news_type'] = 'financenews'
        item['has_img'] = 0
        item['news_link'] = response.xpath('//iframe/@src')
        item['img_url'] = ''
        yield item

    def handle_healthnews(self, response):
        # 健康板块 focus共12条
        focuslistnews_title = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/text()').extract()
        focuslistnews_link = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/@href').extract()
        for i in range(0, len(focuslistnews_title)):
            item = BaiduNewsItem()
            item['title'] = focuslistnews_title[i]
            item['news_type'] = 'healthnews'
            item['has_img'] = 0
            item['news_link'] = focuslistnews_link[i]
            item['img_url'] = ''
            yield item

        # 健康图片板块 共3条
        # mask部分 1条
        imgarea_mask_title = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-title"]/@title').extract()
        imgarea_mask_link = response.xpath('//div[@class="image-mask-item"]/a[@class="item-image"]/@href').extract()
        imgarea_mask_img = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-image"]/img/@src').extract()
        for i in range(0, len(imgarea_mask_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_mask_title[i]
            item['news_type'] = 'healthnews'
            item['has_img'] = 1
            item['news_link'] = imgarea_mask_link[i]
            item['img_url'] = imgarea_mask_img[i]
            yield item

        # 其余部分 2条
        imgarea_title = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        imgarea_link = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        imgarea_img = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(imgarea_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_title[i]
            item['news_type'] = 'healthnews'
            item['has_img'] = 1
            item['news_link'] = imgarea_link[i]
            item['img_url'] = imgarea_img[i]
            yield item

        # 健康话题板块 1条有封面
        topic_top_title = response.xpath(
            '//div[@class="topic-txt"]/h4/a/text()'
        ).extract()
        topic_top_link = response.xpath(
            '//div[@class="topic-pic"]/a/@href'
        ).extract()
        topic_top_img = response.xpath(
            '//div[@class="topic-pic"]/a/img/@src'
        ).extract()
        for i in range(0, len(topic_top_title)):
            item = BaiduNewsItem()
            item['title'] = topic_top_title[i]
            item['news_type'] = 'healthnews'
            item['has_img'] = 1
            item['news_link'] = topic_top_link[i]
            item['img_url'] = topic_top_img[i]
            yield item

        # 健康话题板块 8条无封面
        topic_title = response.xpath(
            '//ul[@class="ulist "]/li/a/text()'
        ).extract()
        topic_link = response.xpath(
            '//ul[@class="ulist "]/li/a/@href'
        ).extract()
        for i in range(0, len(topic_title)):
            item = BaiduNewsItem()
            item['title'] = topic_title[i]
            item['news_type'] = 'healthnews'
            item['has_img'] = 0
            item['news_link'] = topic_link[i]
            item['img_url'] = ''
            yield item

    def handle_internationalnews(self, response):
        # 国际板块 focus共12条
        focuslistnews_title = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/text()').extract()
        focuslistnews_link = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/@href').extract()
        for i in range(0, len(focuslistnews_title)):
            item = BaiduNewsItem()
            item['title'] = focuslistnews_title[i]
            item['news_type'] = 'internationalnews'
            item['has_img'] = 0
            item['news_link'] = focuslistnews_link[i]
            item['img_url'] = ''
            yield item

        # 国际图片板块 共3条
        # mask部分 1条
        imgarea_mask_title = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-title"]/@title').extract()
        imgarea_mask_link = response.xpath('//div[@class="image-mask-item"]/a[@class="item-image"]/@href').extract()
        imgarea_mask_img = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-image"]/img/@src').extract()
        for i in range(0, len(imgarea_mask_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_mask_title[i]
            item['news_type'] = 'internationalnews'
            item['has_img'] = 1
            item['news_link'] = imgarea_mask_link[i]
            item['img_url'] = imgarea_mask_img[i]
            yield item

        # 其余部分 2条
        imgarea_title = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        imgarea_link = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        imgarea_img = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(imgarea_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_title[i]
            item['news_type'] = 'internationalnews'
            item['has_img'] = 1
            item['news_link'] = imgarea_link[i]
            item['img_url'] = imgarea_img[i]
            yield item

        # 环球视野板块 2条有封面
        topic_top_title = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        topic_top_link = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        topic_top_img = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(topic_top_title)):
            item = BaiduNewsItem()
            item['title'] = topic_top_title[i]
            item['news_type'] = 'internationalnews'
            item['has_img'] = 1
            item['news_link'] = topic_top_link[i]
            item['img_url'] = topic_top_img[i]
            yield item

        # 国际热搜词
        hotclick_title = response.xpath(
            '//ol[contains(@class, "olist")]/li/a/@title'
        ).extract()
        hotclick_link = response.xpath(
            '//ol[contains(@class, "olist")]/li/a/@href'
        ).extract()
        for i in range(0, len(hotclick_title)):
            item = BaiduNewsItem()
            item['title'] = hotclick_title[i]
            item['news_type'] = 'internationalnews'
            item['has_img'] = 0
            item['news_link'] = hotclick_link[i]
            item['img_url'] = ''
            yield item

    def handle_internetnews(self, response):
        # 互联网板块 focus共12条
        focuslistnews_title = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/text()').extract()
        focuslistnews_link = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/@href').extract()
        for i in range(0, len(focuslistnews_title)):
            item = BaiduNewsItem()
            item['title'] = focuslistnews_title[i]
            item['news_type'] = 'internetnews'
            item['has_img'] = 0
            item['news_link'] = focuslistnews_link[i]
            item['img_url'] = ''
            yield item

        # 国际图片板块 共3条
        # mask部分 1条
        imgarea_mask_title = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-title"]/@title').extract()
        imgarea_mask_link = response.xpath('//div[@class="image-mask-item"]/a[@class="item-image"]/@href').extract()
        imgarea_mask_img = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-image"]/img/@src').extract()
        for i in range(0, len(imgarea_mask_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_mask_title[i]
            item['news_type'] = 'internetnews'
            item['has_img'] = 1
            item['news_link'] = imgarea_mask_link[i]
            item['img_url'] = imgarea_mask_img[i]
            yield item

        # 其余部分 2条
        imgarea_title = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        imgarea_link = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        imgarea_img = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(imgarea_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_title[i]
            item['news_type'] = 'internetnews'
            item['has_img'] = 1
            item['news_link'] = imgarea_link[i]
            item['img_url'] = imgarea_img[i]
            yield item

        # 公司、人物动态 10条
        topic_title = response.xpath(
            '//ul[@class="ulist "]/li/a/text()'
        ).extract()
        topic_link = response.xpath(
            '//ul[@class="ulist "]/li/a/@href'
        ).extract()
        for i in range(0, len(topic_title)):
            item = BaiduNewsItem()
            item['title'] = topic_title[i]
            item['news_type'] = 'internetnews'
            item['has_img'] = 0
            item['news_link'] = topic_link[i]
            item['img_url'] = ''
            yield item

    def handle_ladynews(self, response):
        # 女人板块 focus共12条
        focuslistnews_title = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/text()').extract()
        focuslistnews_link = response.xpath('//ul[contains(@class, "focuslistnews")]/li/a/@href').extract()
        for i in range(0, len(focuslistnews_title)):
            item = BaiduNewsItem()
            item['title'] = focuslistnews_title[i]
            item['news_type'] = 'ladynews'
            item['has_img'] = 0
            item['news_link'] = focuslistnews_link[i]
            item['img_url'] = ''
            yield item

        # 女人图片板块 共3条
        # mask部分 1条
        imgarea_mask_title = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-title"]/@title').extract()
        imgarea_mask_link = response.xpath('//div[@class="image-mask-item"]/a[@class="item-image"]/@href').extract()
        imgarea_mask_img = response.xpath(
            '//div[@class="image-mask-item"]/a[@class="item-image"]/img/@src').extract()
        for i in range(0, len(imgarea_mask_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_mask_title[i]
            item['news_type'] = 'ladynews'
            item['has_img'] = 1
            item['news_link'] = imgarea_mask_link[i]
            item['img_url'] = imgarea_mask_img[i]
            yield item

        # 其余部分 2条
        imgarea_title = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        imgarea_link = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        imgarea_img = response.xpath(
            '//div[@class="imagearea-bottom"]/div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(imgarea_title)):
            item = BaiduNewsItem()
            item['title'] = imgarea_title[i]
            item['news_type'] = 'ladynews'
            item['has_img'] = 1
            item['news_link'] = imgarea_link[i]
            item['img_url'] = imgarea_img[i]
            yield item

        # 星座板块 1条有封面
        topic_top_title = response.xpath(
            '//div[@class="topic-txt"]/h4/a/text()'
        ).extract()
        topic_top_link = response.xpath(
            '//div[@class="topic-pic"]/a/@href'
        ).extract()
        topic_top_img = response.xpath(
            '//div[@class="topic-pic"]/a/img/@src'
        ).extract()
        for i in range(0, len(topic_top_title)):
            item = BaiduNewsItem()
            item['title'] = topic_top_title[i]
            item['news_type'] = 'ladynews'
            item['has_img'] = 1
            item['news_link'] = topic_top_link[i]
            item['img_url'] = topic_top_img[i]
            yield item

        # 详细板块 8条无封面
        topic_title = response.xpath(
            '//ul[@class="ulist "]/li/a/text()'
        ).extract()
        topic_link = response.xpath(
            '//ul[@class="ulist "]/li/a/@href'
        ).extract()
        for i in range(0, len(topic_title)):
            item = BaiduNewsItem()
            item['title'] = topic_title[i]
            item['news_type'] = 'ladynews'
            item['has_img'] = 0
            item['news_link'] = topic_link[i]
            item['img_url'] = ''
            yield item

        # 底部图文
        imglist_title = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/@title'
        ).extract()
        imglist_link = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/@href'
        ).extract()
        imglist_img = response.xpath(
            '//div[@class="image-list"]//div[@class="image-list-item"]/a[@title]/img/@src'
        ).extract()
        for i in range(0, len(imglist_title)):
            item = BaiduNewsItem()
            item['title'] = imglist_title[i]
            item['news_type'] = 'ladynews'
            item['has_img'] = 1
            item['news_link'] = imglist_link[i]
            item['img_url'] = imglist_img[i]
            yield item

    def handle_localnews(self, response):
        # localnews用ajax获取, 理应再存一个城市名字的，暂略
        result = json.loads(response.text)
        data = result['data']['LocalNews']['data']['rows']
        data_pic = data['pic']
        item = BaiduNewsItem()
        item['title'] = data_pic['title']
        item['news_type'] = 'localnews'
        item['has_img'] = 1
        item['news_link'] = data_pic['url']
        item['img_url'] = data_pic['imgurl']
        yield item

        data_first = data['first']
        for news in data_first:
            item = BaiduNewsItem()
            item['title'] = news['title']
            item['news_type'] = 'localnews'
            item['has_img'] = 0
            item['news_link'] = news['url']
            item['img_url'] = ''
            yield item

        data_second = data['second']
        for news in data_second:
            item = BaiduNewsItem()
            item['title'] = news['title']
            item['news_type'] = 'localnews'
            item['has_img'] = 0
            item['news_link'] = news['url']
            item['img_url'] = ''
            yield item

        # time.sleep(60)
        # new_url ='http://news.baidu.com/widget?id=LocalNews&ajax=json&t={0}'.format(int(time.time()*1000))
        # yield scrapy.Request(url=new_url, dont_filter=True, headers=self.headers,
        #                      callback=self.handle_localnews)

    def handle_militarynews(self, response):
        # 军事
        result = json.loads(response.text)
        data = result['data']['MilitaryNews']
        focusNews = data['focusNews']
        picNews = data['picNews']
        tophit = data['tophit']
        chinamilitary = data['chinamilitary']
        for news in focusNews:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'militarynews'
            item['has_img'] = 0
            item['news_link'] = news['m_url']
            item['img_url'] = ''
            yield item

        for news in picNews:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'militarynews'
            item['has_img'] = 1
            item['news_link'] = news['m_url']
            item['img_url'] = news['m_image_url']
            yield item

        for news in tophit:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'militarynews'
            item['has_img'] = 0
            item['news_link'] = news['m_url']
            item['img_url'] = ''
            yield item

        for news in chinamilitary:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'militarynews'
            item['has_img'] = 0
            item['news_link'] = news['m_url']
            item['img_url'] = ''
            yield item
        pass

    def handle_picwall(self, response):
        # 图片新闻
        result = json.loads(response.text)
        data = result['data']['PicWall']
        picwall = data['PicWall']

        for news in picwall:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'picwall'
            item['has_img'] = 1
            item['news_link'] = news['m_url']
            item['img_url'] = news['m_image_url']
            yield item
        # time.sleep(60)
        # yield scrapy.Request()

    def handle_sportnews(self, response):
        # 体育
        result = json.loads(response.text)
        data = result['data']['SportNews']
        focusNews = data['focusNews']
        picNews = data['picNews']
        nba = data['NBA']
        topicNews = data['topicNews']
        for news in focusNews:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'sportnews'
            item['has_img'] = 0
            item['news_link'] = news['m_url']
            item['img_url'] = ''
            yield item

        for news in picNews:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'sportnews'
            item['has_img'] = 1
            item['news_link'] = news['m_url']
            item['img_url'] = news['m_image_url']
            yield item

        for news in nba:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'sportnews'
            item['has_img'] = 1
            item['news_link'] = news['m_url']
            item['img_url'] = news['m_image_url']
            yield item

        for news in topicNews:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'sportnews'
            item['has_img'] = 0
            item['news_link'] = news['m_url']
            item['img_url'] = ''
            yield item
        pass

    def handle_technews(self, response):
        result = json.loads(response.text)
        data = result['data']['TechNews']
        focusNews = data['focusNews']
        picNews = data['picNews']
        topicNews_pic = data['topicNews']['picNews']
        topicNews_focus = data['topicNews']['picNews']
        for news in focusNews:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'technews'
            item['has_img'] = 0
            item['news_link'] = news['m_url']
            item['img_url'] = ''
            yield item

        for news in picNews:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'technews'
            item['has_img'] = 1
            item['news_link'] = news['m_url']
            item['img_url'] = news['m_image_url']
            yield item

        for news in topicNews_pic:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'technews'
            item['has_img'] = 1
            item['news_link'] = news['m_url']
            item['img_url'] = news['m_image_url']
            yield item

        for news in topicNews_focus:
            item = BaiduNewsItem()
            item['title'] = news['m_title']
            item['news_type'] = 'technews'
            item['has_img'] = 0
            item['news_link'] = news['m_url']
            item['img_url'] = ''
            yield item
        pass

