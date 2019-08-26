# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/8/13 23:21"


if __name__ == '__main__':

    import time
    import re

    import requests
    from lxml import etree

    keyword = input()

    url = "https://s.taobao.com/search?q={0}&s={1}".format(keyword, 0)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    # cookies已改
    cookies = {
        "cna": "wP0KE+2qJDQCAbfr/zTkf508",
        "tracknick": "*****",
        "tg": "0",
        "enc": "kXU1Oznuh7EKujVeJkCQrY7l5c6dmL7XBHx6TlGRMdxf9XUBGrDUSuFkEZkpl4KBjZDgvC3rb8fc6R%2BM%2FnyMCw%3D%3D",
        "x": "e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0",
        "miid": "997349820532202908",
        "t": "2751601abdaadd6683fcf8d11c642e73",
        "hng": "CN%7Czh-CN%7CCNY%7C156",
        "thw": "cn",
        "v": "0",
        "cookie2": "1c1120e47d310e8d32e7c7b2760c41a4",
        "_tb_token_": "556eb7e6e891e",
        "SL_GWPT_Show_Hide_tmp": "1",
        "SL_wptGlobTipTmp": "1",
        "unb": "2324752842",
        "uc3": "nk2=FP8q42o2wUQ%3D&id2=UUtJY9YkN1VVoQ%3D%3D&lg2=URm48syIIVrSKA%3D%3D&vt3=F8dBy3KxJBf2zWWPCh8%3D",
        "csg": "98f47fe4",
        "lgc": "*****",
        "cookie17": "UUtJY9YkN1VVoQ%3D%3D",
        "dnk": "*****",
        "skt": "7fcbca50c35a7b82",
        "existShop": "MTU2NTcxMTI5Mg%3D%3D",
        "uc4": "id4=0%40U2lzTQEwzBAGAHpvN3Jd46lW%2BZlB&nk4=0%40FnQqYbDIpwH4ohZE%2Bs1HsAeE1w%3D%3D",
        "_cc_": "Vq8l%2BKCLiw%3D%3D",
        "_l_g_": "Ug%3D%3D",
        "sg": "52e",
        "_nk_": "*****",
        "cookie1": "W8nSZDlx3MkUwqSpn7oaCPXTUdrl4pmKsTTtCrOB9g0%3D",
        "mt": "ci=44_1",
        "uc1": "cookie14=UoTaHYnQoto0xA%3D%3D&lng=zh_CN&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&existShop=false&cookie21=U%2BGCWk%2F7pY%2FF&tag=8&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0",
        "whl": "-1%260%260%261565711693750",
        "isg": "BJeXusoYhrzorwWHYhBECH82JgshdGtYLAscXenEs2bNGLda8az7jlU6evij60O2",
        "l": "cBIl2Dgqv_uyc2RkBOCanurza77OSIRYYuPzaNbMi_5ar6TsNa7Ok-5HgF96VjWd9b8B4YInwjp9-etkZx75B4--g3fP"
    }
    # 得到第一页搜索结果
    response = requests.get(url, headers=headers, cookies=cookies)
    # selector = etree.HTML(response.text)
    # 图片链接
    # img_linklist = selector.xpath('//div[contains(@class, "item J_MouserOnverReq")]//img/@src')

    # html源码写在了script上，因此用xpath提取不到，所以改用正则
    pic_url_pat = re.compile('"pic_url":"(.*?)"')
    pic_url_list = pic_url_pat.findall(response.text)

    count = 0
    for pic_url in pic_url_list:
        # 逻辑：打开图片链接，保存为本地文件。暂不做
        print(pic_url)
        count += 1
    print(count)

    # 是否有下一页
    try:
        # next_s = selector.xpath('//li[contains(@class, "item next")]/a/@data-value')
        page_pat = re.compile('"totalPage":(\d+)')
        total_page = int(page_pat.findall(response.text)[0])
        next_s = 44
        while next_s <= total_page*44:
            print("有下一页")
            url = "https://s.taobao.com/search?q={0}&s={1}".format(keyword, next_s)
            time.sleep(2)
            response = requests.get(url, headers=headers, cookies=cookies)
            # selector = etree.HTML(response.text)
            # 图片链接
            pic_url_list = pic_url_pat.findall(response.text)
            for pic_url in pic_url_list:
                # 逻辑：打开图片链接，保存为本地文件。空间太大，暂不做
                print(pic_url)
                count += 1
            next_s = next_s + 44
            print(count)
    except Exception as e:
        print(type(e))
        print(e)


