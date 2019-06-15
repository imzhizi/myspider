# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from myspider.models import DoubanModel


class MyspiderItem(scrapy.Item):
    title = scrapy.Field()
    douban_link = scrapy.Field()
    rating = scrapy.Field()

    # 我使用的db是 elasticsearch
    def save_to_db(self):
        douban = DoubanModel()

        douban.title = self['title']
        douban.douban_link = self['douban_link']
        douban.rating = self['rating']

        douban.save()

        return douban
