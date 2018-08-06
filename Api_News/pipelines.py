# -*- coding: utf-8 -*-
from .items import JSModel
from Api_News.items import ApiNewsItem, NewsImageItem
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class ApiNewsPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ApiNewsItem):
            if not JSModel.table_exists():
                pass
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
                JSModel.insert(data).execute()
            except Exception as e:
                if str(e.args[0]) == '1062':
                    print('Duplication of data')
                else:
                    print(e.args[0], e.args[1])

            return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        if isinstance(item, NewsImageItem):
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None):
        image_guid = request.url
        name = str(image_guid).split('/')[-1]
        return 'full/%s' % name

