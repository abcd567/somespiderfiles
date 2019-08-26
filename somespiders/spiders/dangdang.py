# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from somespiders.items import DangdangItem
from somespiders.utils.common import get_md5

class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/cid4008149.html']

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
        "ITEM_PIPELINES": {
            'somespiders.pipelines.MySQLPileline': 300,
        }
    }

    def parse(self, response):
        # item = DangdangItem() # item写在这个位置不行！！！！

        title = response.xpath('//p[@class="name"]/a/text()').extract()
        link = response.xpath('//p[@class="name"]/a/@href').extract()
        price = response.xpath('//p[@class="price"]/span[@class="price_n"]/text()').extract()

        for i in range(0, len(title)):
            item = DangdangItem()   # item 必须写在这里，和创建空列表一样！！！
            item['title'] = title[i]
            item['link'] = link[i]
            item['price'] = price[i]
            item['link_md5'] = get_md5(link[i])
            yield item

        for i in range(0, 100):
            # 一页48条数据，一共能找到100页，共4800条数据
            url = 'http://category.dangdang.com/pg{page}-cid4008149.html'.format(page=i+1)
            yield Request(url, callback=self.parse)
        pass
