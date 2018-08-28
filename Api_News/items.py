# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from peewee import *

db = MySQLDatabase("station", host='23.110.211.170', port=3339, user='station', passwd='123456', charset='utf8')
# db = MySQLDatabase("station", host='127.0.0.1', port=3306, user='root', passwd='123456', charset='utf8')
# db = MySQLDatabase("alizhizhuchi", host='23.110.211.170', port=3339, user='alizhizhuchi', passwd='3b86aba28d1ffc65', charset='utf8')
# db = MySQLDatabase("alizhizhuchi", host='142.234.162.99', port=3339, user='alizhizhuchi', passwd='c7196f1d85e99200', charset='utf8')


class ApiNewsItem(scrapy.Item):
    re_id = scrapy.Field()
    dataType = scrapy.Field()
    pageToken = scrapy.Field()
    hasNext = scrapy.Field()
    videoUrls = scrapy.Field()
    tags = scrapy.Field()
    description = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    image = scrapy.Field()
    publishDateStr = scrapy.Field()
    quantity = scrapy.Field()
    content = scrapy.Field()
    likeCount = scrapy.Field()
    viewCount = scrapy.Field()


class JSModel(Model):
    re_id = CharField(max_length=100, unique=True)
    author = CharField(max_length=100)
    title = CharField(max_length=200)
    keyword = CharField(max_length=200)
    description = TextField()
    create_time = DateTimeField(formats='%Y-%m-%d %H:%M:%S')
    quantity = IntegerField()
    read = IntegerField()
    comment = IntegerField()
    like = IntegerField()
    img = TextField()
    videoUrls = TextField(default='1.mp4')
    context = TextField()
    url = CharField(max_length=200)
    tips = CharField(max_length=100)
    source = CharField(max_length=200)

    class Meta:
        table_name = 'JSModel_newsarticle'
        database = db


class AliTitle(Model):
    title = CharField(max_length=255, unique=True)
    content = TextField()
    yuan_id = IntegerField()
    object_id = IntegerField()
    caiji_id = IntegerField()

    class Meta:
        table_name = 'c_title'
        database = db


# image item
class NewsImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()






