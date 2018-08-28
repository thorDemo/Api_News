# -*- coding:utf-8 -*-
import scrapy
import json
from Api_News.items import ApiNewsItem, NewsImageItem
from snownlp import SnowNLP
import hashlib
from scrapy.utils.python import to_bytes

video = open('video.txt', 'w+')


class ApinewsSpider(scrapy.Spider):
    name = 'ApiNews'
    allowed_domains = ['47.90.63.143']
    api = 'OrTqAiyVROsmXuQMR6Lmr7eENi5GZX7o6swyVh1KcHHu7nGccWjTgLEBWW7WtqVD'
    start_urls = [
        # 美食
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=0&catid=3&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=20&catid=3&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=40&catid=3&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=60&catid=3&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=80&catid=3&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=100&catid=3&apikey=%s' % api,
        # 娱乐
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=0&catid=10028&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=20&catid=10028&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=40&catid=10028&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=60&catid=10028&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=80&catid=10028&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=100&catid=10028&apikey=%s' % api,
        # 体育
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=0&catid=100213&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=20&catid=100213&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=40&catid=100213&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=60&catid=100213&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=80&catid=100213&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=100&catid=100213&apikey=%s' % api,
        # 赛马
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=0&catid=100214&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=20&catid=100214&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=40&catid=100214&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=60&catid=100214&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=80&catid=100214&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=100&catid=100214&apikey=%s' % api,
        # 焦点
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=0&catid=0&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=20&catid=0&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=40&catid=0&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=60&catid=0&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=80&catid=0&apikey=%s' % api,
        'https://47.90.63.143/news/appledailyhk?type=2&pageToken=100&catid=0&apikey=%s' % api,
    ]

    def parse(self, response):
        print(response.url)
        item = ApiNewsItem()
        image_item = NewsImageItem()
        result = json.loads(response.text)

        try:
            has_next = result['hasNext']
            print(has_next)
        except TypeError:
            print('没有数据！')
            return
        if str(response.url).count('catid=0'):
            item['dataType'] = 'jiaodian'
        elif str(response.url).count('catid=100214'):
            item['dataType'] = 'saima'
        elif str(response.url).count('catid=100213'):
            item['dataType'] = 'tiyu'
        elif str(response.url).count('catid=10028'):
            item['dataType'] = 'yule'
        elif str(response.url).count('catid=3'):
            item['dataType'] = 'meishi'

        item['author'] = result['appCode']
        for news in result['data']:
            if not news['videoUrls']:
                news['videoUrls'] = 'no'
            try:
                images = ''
                for img in news['imageUrls']:
                    images += hashlib.sha1(to_bytes(img)).hexdigest() + '.jpg,'
                images = images.strip(',')
                item['image'] = images
                for image in news['imageUrls']:
                    image_item['image_urls'] = [image]
                    yield image_item
            except TypeError:
                pass
            item['re_id'] = news['id']
            videos = str(news['videoUrls']).replace('\'', '').strip(']').replace('[', '').split(',')
            print(videos)
            item['videoUrls'] = videos
            for line in videos:
                if line == 'no':
                    continue
                video.write(line.strip() + '\n')
            item['tags'] = SnowNLP(','.join(i for i in news['tags'])).han
            item['title'] = SnowNLP(news['title']).han

            item['publishDateStr'] = str(news['publishDateStr']).replace('T', ' ')
            item['quantity'] = self.comment_quantity(news['content'])
            item['content'] = SnowNLP(news['content']).han
            item['description'] = SnowNLP(item['content']).summary(3)
            item['likeCount'] = news['likeCount']
            item['viewCount'] = news['viewCount']
            yield item

    def comment_quantity(self, value):
        length = len(value)
        utf8_length = len(value.encode('utf-8'))
        length = (utf8_length - length) / 2 + length
        return length
