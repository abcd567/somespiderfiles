# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/8/15 19:38"


if __name__ == '__main__':

    import time
    import re
    import json

    import requests

    from somespiders.utils.ua_pool import ua_pool

    # targetid 可以通过网页的评论块获取到
    # last 是下十个评论的编号起始取0即可
    # 琅琊榜的tid
    targetid = '1210555765'
    start_url = "https://video.coral.qq.com/varticle/{targetid}/comment/v2?orinum=10&oriorder=o&pageflag=1&cursor={cursor}".format(targetid=targetid, cursor=0)

    response = requests.get(url=start_url, headers=ua_pool())
    data_dict = json.loads(response.text)

    # 提取first cursor
    first_cursor = data_dict['data']['first']
    # 由first cursor构造url
    first_url = "https://video.coral.qq.com/varticle/{targetid}/comment/v2?orinum=10&oriorder=o&pageflag=1&cursor={cursor}".format(
        targetid=targetid, cursor=first_cursor)

    time.sleep(1)
    response = requests.get(url=first_url, headers=ua_pool())
    data_dict = json.loads(response.text)

    # 是否有下一页
    while data_dict['data']['hasnext']:
        # 有下一页
        # 构造下一页url
        last_url = "https://video.coral.qq.com/varticle/{targetid}/comment/v2?orinum=10&oriorder=o&pageflag=1&cursor={cursor}".format(
            targetid=targetid, cursor=data_dict['data']['last'])
        # 提取本页评论
        comment_list = []
        for comment in data_dict['data']['oriCommList']:
            comment_list.append(comment['content'])
            print('评论内容：' + comment['content'])

        # 可以在这个位置将comment_list的内容入库或是写入文件
        #
        #
        #

        print()
        print('-----------------------------------下一页-----------------------------------：')
        print()

        time.sleep(2)
        response = requests.get(url=last_url, headers=ua_pool())
        data_dict = json.loads(response.text)

    print('没有更多了~')
