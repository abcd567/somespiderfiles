# _*_ coding: utf-8 _*_
__author__ = "吴飞鸿"
__date__ = "2019/8/11 16:43"

if __name__ == '__main__':

    import requests
    from lxml import etree

    url = "https://blog.csdn.net"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.text)
    titles = selector.xpath('//ul[@class="feedlist_mod home"]/li//div[@class="title"]/h2/a/text()')
    hrefs = selector.xpath('//ul[@class="feedlist_mod home"]/li//div[@class="title"]/h2/a/@href')
    news_list = []
    for i in range(0, len(titles)):
        news = {}
        news['title'] = titles[i].replace('\n', '').strip(' ')
        news['link'] = hrefs[i]
        news_list.append(news)

    for news in news_list:
        url = news['link']
        response = requests.get(url,headers=headers)
        with open('csdn_blog_news_html/{0}.html'.format(news['title']), 'wb') as f:
            f.write(response.content)

    print("结束！！")