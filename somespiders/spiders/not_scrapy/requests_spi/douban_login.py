# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/8/17 23:48"


import requests

from somespiders.utils.ua_pool import ua_pool

if __name__ == '__main__':
    form_data = {
        'ck': '',
        'name': '159****4115',
        'password': 'slzk******',
        'remember': 'false',
        'ticket': ''
    }
    response = requests.post(
        url='https://accounts.douban.com/j/mobile/login/basic',
        data= form_data,
        headers= ua_pool()
    )

    print(response.text)

    # 成了，数据没问题
