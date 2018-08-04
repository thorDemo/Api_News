# -*- coding: utf-8 -*-
from .items import JSModel_newsarticle
from Api_News.items import ApiNewsItem, NewsImageItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy


class ApiNewsPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ApiNewsItem):
            if not JSModel_newsarticle.table_exists():
                JSModel_newsarticle.create_table()
            try:
                data = {
                    're_id': item['re_id'],
                    'author': item['author'],
                    'title': item['title'],
                    'keyword': item['tags'],
                    'description': item['description'],
                    'create_time': item['publishDateStr'],
                    'quantity': item['quantity'],
                    'read': item['viewCount'],
                    'comment': 0,
                    'like': item['likeCount'],
                    'img': item['image'],
                    'context': item['content'],
                    'url': '/show/%s/' % item['re_id'],
                    'tips': item['dataType'],
                    'source': 'S1',
                    'videoUrls': item['videoUrls'],
                }
                JSModel_newsarticle.insert_many(data).execute()
            except Exception as e:
                if str(e.args[0]) == '1062':
                    print('重复数据，跳过。')
                else:
                    print(e.args[0], e.args[1])

            return item


class MyImagesPipeline(ImagesPipeline):
    """自定义图片下载器,以图片url为路径保存图片"""
    def get_media_requests(self, item, info):
        """
        发生图片下载请求,其中item['front_image_url']字段是scrapy中我们自定义的url字段,
        以数组的方式存储,遍历数组请求图片
        """
        if isinstance(item, NewsImageItem):
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url)

    # def item_completed(self, results, item, info):
    #     """
    #     results是一个list 第一个为图片下载状态,对应OK  第二个是一个tupled其中可以为path的字段对应存储路径,
    #     而item['front_image_path']是我们自定义字段,保存在item中
    #     """
    #     if isinstance(item, NewsImageItem):
    #         front_image_path = [x['path'] for ok, x in results if ok]
    #         if not front_image_path:
    #             raise DropItem("Item contains no images")
    #         item['front_image_path'] = front_image_path
    #         return item

    def file_path(self, request, response=None, info=None):
        """自定义图片保存路径,以图片的url保存,重写前是图片的url经过MD5编码后存储"""
        image_guid = request.url
        name = str(image_guid).split('/')[-1]
        return 'full/%s' % name

