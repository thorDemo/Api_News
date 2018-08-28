# -*- coding:utf-8 -*-
import scrapy


class ApinewsSpider(scrapy.Spider):
    """
    算法1 ：b  算法2 ：y  算法3 ：by
    算法4 ：yb 算法5 ：g  算法6 ：gy
    算法7 ：yg 算法8 ：gb 算法9 ：bg
    """
    name = 'Baidu'
    allowed_domains = ['www.alizhizhuchi.com']


    def start_requests(self):
        content = 'CDPR其实还带来了另一部视频，它包含了《巫师3》游戏的有趣开发幕后，游戏中各种搞笑的Bug和恶搞作品。果然官方鬼畜最为致命'
        form_request = scrapy.http.FormRequest(url='http://www.alizhizhuchi.com/weiyuanchuang/', formdata={'t': 'b', 'q': content, 'k': 'a'}, callback=self.parse)
        yield form_request

    def parse(self, response):
        print(response.text)
