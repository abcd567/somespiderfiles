# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/8/14 20:31"


if __name__ == '__main__':

    import time
    import re

    import requests
    from lxml import etree

    from somespiders.utils.ua_pool import ua_pool

    # 输入查询关键字,python
    # keyword = input()
    keyword = 'python'
    start_url = 'https://weixin.sogou.com/weixin?query={query}&type=2&page={page}&ie=utf8'.format(query=keyword, page=1)

    response = requests.get(start_url, headers=ua_pool())

    pat = re.compile('data-share="(.*?)"')
    rst_list = pat.findall(response.text)
    print(response.text)
    print(rst_list)
    """
     IP又被封了！！！！！！操
    """

