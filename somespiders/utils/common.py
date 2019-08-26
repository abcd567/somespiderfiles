# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/8/17 17:36"

import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()