# _*_ coding: utf-8 _*_


__author__ = "吴飞鸿"
__date__ = "2019/8/9 22:33"


if __name__ == '__main__':

    import re
    from urllib.parse import urljoin

    import requests
    from lxml import etree
    import pymongo

    data = requests.get('https://read.douban.com/provider/all').text
    selector = etree.HTML(data)
    # 地址
    href = selector.xpath("//div[@class='provider-list']//ul//@href")
    href_list = []
    for h in href:
        href_list.append(urljoin('https://read.douban.com/provider/all', h))
    # 图片
    image = selector.xpath("//div[@class='provider-list']//div[@class='avatar']/img/@src")
    # 出版社名字
    name = selector.xpath("//div[@class='provider-list']//div[@class='name']/text()")
    # 在售作品数量
    nums = selector.xpath("//div[@class='provider-list']//div[@class='works-num']/text()")
    pat = re.compile("(\d+) 部作品在售")
    num_list = []
    for num in nums:
        num = pat.findall(num)
        num_list.append(num[0])

    # print(len(href), len(image), len(name), len(num_list))

    # 组装字典,#入mongodb

    dict_list = []
    for i in range(0, len(href)):
        dict = {}
        dict["name"] = name[i]
        dict['href'] = href_list[i]
        dict['image'] = image[i]
        dict['work_num'] = str(num_list[i])
        dict_list.append(dict)

    # # 连接本地数据库
    # mongo_py = pymongo.MongoClient()
    # # 建数据库
    # db = mongo_py['read_douban']
    # # 建集合
    # collection = db['read_douban']
    # # 插入数据库
    # collection.insert_many(dict_list)

    print(dict_list)

