# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/8/25 21:15"

import urllib.request
import re

import redis
import pymysql
from lxml import etree

rdconn = redis.Redis('172.17.0.2', '6379')
# mysql_conn = pymysql.connect('172.17.0.2', 'wfh', '123456', 'nov_17k', charset="utf8", use_unicode=True)
# cursor = mysql_conn.cursor()


for i in range(1, 335):
    url = 'https://www.17k.com/all/book/2_0_0_0_0_0_0_0_{0}.html'.format(str(i))
    isdone = rdconn.hget('url', str(i))
    if isdone:
        continue
    rdconn.hset('url', str(i), '1')
    try:
        data = urllib.request.urlopen(url=url).read().decode('utf8', 'ignore')
        selector = etree.HTML(data)
        book_list = selector.xpath('//tbody/tr[@class]/td[@class="td3"]/span/a/text()')
        link_list = selector.xpath('//tbody/tr[@class]/td[@class="td3"]/span/a/@href')

        # for j in range(0, len(book_list)):
        #     insert_sql = """
        #                 insert into nov_17k(bookname, link)
        #                 VALUES (%s, %s)
        #           """
        #     cursor.execute(insert_sql, (book_list[j], link_list[j]))
        #     mysql_conn.commit()
    except Exception as err:
        print(str(i), err)
        continue

    for j in range(0, len(book_list)):
        rdconn.hset('rst', str((i-1)*30 + j + 1), book_list[j])
