# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/8/17 17:10"

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(["scrapy", "crawl", "dangdang"])

execute(["scrapy", "crawl", "douban_login"])

# execute(["scrapy", "crawl", "news_baidu"])

