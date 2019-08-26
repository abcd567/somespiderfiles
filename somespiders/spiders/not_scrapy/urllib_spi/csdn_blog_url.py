# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/8/11 16:38"


if __name__ == '__main__':

    from urllib import request

    url = "https://blog.csdn.net"

    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome\
    /74.0.3729.169 Safari/537.36")
    opener = request.build_opener()
    opener.addheaders = [headers]
    data = opener.open(url).read().decode("utf8")
    print(data)
