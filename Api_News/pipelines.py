# -*- coding: utf-8 -*-
from .items import JSModel, AliTitle
from Api_News.items import ApiNewsItem, NewsImageItem
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import re


class ApiNewsPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ApiNewsItem):
            if not JSModel.table_exists():
                JSModel.create_table()
            # if not AliTitle.table_exists():
            #     AliTitle.create_table()
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
                # content = str(item['content'])
                # content.replace('\n', '')
                # content = content.split('立即免费下载《饮食男女》')[0]
                # content.replace('资料来源：台湾《苹果日报》', '')
                # text = re.findall(r'.{70}', content)
                # text.append(content[(len(text)*70):])
                # images = str(item['image']).split(',')
                # video = item['videoUrls']
                # images += video
                # result = []
                # for line in text:
                #     result.append('<p>%s</p>' % line)
                # text_num = len(result)
                # x = 0
                # for line in images:
                #     if 'jpg' in line :
                #         result.insert(int(text_num / len(images)) * x, '<img src="/tupian_1/%s"></img>' % line)
                #     elif 'no' == line:
                #         pass
                #     else:
                #         vi = '<video width="320" height="240" controls>' \
                #              '<source src="%s" type="video/mp4">' \
                #              '</video>' % line
                #         result.insert(int(text_num / len(images)) * x, vi)
                #     x += 1
                # content = ''
                # for line in result:
                #     content += line + '\n'
                # data = {
                #     'title': item['title'],
                #     'content': content,
                #     'yuan_id': 2,
                #     'object_id': 25,
                #     'caiji_id': 0,
                # }
                # # print(data)
                # AliTitle.insert(data).execute()
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

    # def file_path(self, request, response=None, info=None):
    #     image_guid = request.url
    #     name = str(image_guid).split('/')[-1]
    #     return 'full/%s' % name

