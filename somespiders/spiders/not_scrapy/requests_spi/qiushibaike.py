# _*_ coding: utf-8 _*_


__author__ = "吴飞鸿"
__date__ = "2019/8/13 1:09"


if __name__ == '__main__':

    from urllib.parse import urljoin
    import time

    import requests
    from lxml import etree

    url = "https://www.qiushibaike.com/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.text)

    count = 0
    article_linklist = selector.xpath("//li[contains(@class, 'item typs')]/a[@class]/@href")
    for article_link in article_linklist:
        # article_response = requests.get(urljoin(url, article_link))
        # article_seletor = etree.HTML(article_response.text)
        # """
        #     其实应该分类处理，//li[contains(@class, 'item typs')]，有说明 ：
        #     item typs_video
        #     item typs_multi
        #     item typs_word
        #     item typs_image
        #
        #
        # """
        # word = article_seletor.xpath('//div[@class="content"]/text()')
        # print(word)

        print(urljoin(url, article_link))
        count += 1

    try:
        next = selector.xpath('//a/span[@class="next"]/text()')[0]
        while '下一页' in next:
            next_url = selector.xpath('//ul[@class="pagination"]/li[last()]/a/@href')[0]
            next_url = urljoin(url, next_url)

            time.sleep(2)

            response = requests.get(next_url, headers=headers)
            selector = etree.HTML(response.text)

            article_linklist = selector.xpath("//li[contains(@class, 'item typs')]/a[@class]/@href")
            for article_link in article_linklist:
                print(urljoin(url, article_link))
                count += 1

            print(count)
            next = selector.xpath('//a/span[@class="next"]/text()')[0]
        print("End")

    except Exception as e:
        print(e)