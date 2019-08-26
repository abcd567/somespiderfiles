# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SomespidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DangdangItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    link_md5 = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into dangdang_dress(title, link, price, md5)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE title=VALUES(title), price=VALUES(price)
        """

        parmas = (
            self['title'], self['link'], self['price'], self['link_md5']
        )

        return insert_sql, parmas


class BaiduNewsItem(scrapy.Item):
    # # mongo数据库连接部分
    # db_name = 'news'
    # collection_name = 'baidu'

    # # cv版块
    # cv_title = scrapy.Field()
    # cv_link = scrapy.Field()
    # cv_img_title = scrapy.Field()
    # cv_img_link = scrapy.Field()
    # cv_img_picurl = scrapy.Field()

    # MysqlDB
    title = scrapy.Field()
    news_type = scrapy.Field()
    has_img = scrapy.Field()
    news_link = scrapy.Field()
    img_url = scrapy.Field()
    # 包装成一个dict

    def get_insert_sql(self):
        insert_sql = """
                    insert into baidu_news(title, news_type, has_img, news_link, img_url)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE news_type=VALUES(news_type), news_link=VALUES(news_link), img_url=VALUES(img_url)
                """

        parmas = (
            self['title'], self['news_type'], self['has_img'], self['news_link'], self['img_url']
        )

        return insert_sql, parmas
