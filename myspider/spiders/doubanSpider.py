# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy import Request

from myspider.items import MyspiderItem


class DoubanspiderSpider(scrapy.Spider):
    name = 'doubanSpider'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # 找出页面中每个电影的 url
        subjects_nodes = response.css(".item")
        for subject in subjects_nodes:
            # 封面图片的 url
            img_url = subject.css("div > a > img::attr(src)").extract_first()
            subject_url = subject.css("div > a::attr(href)").extract_first()
            # 通过 meta 传递下去
            yield Request(url=parse.urljoin(response.url, subject_url), meta={"front_image_url": img_url},
                          callback=self.parse_detail)

        # 找到下一页 url, 递归调用
        next_url = response.css(".next > a::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    @staticmethod
    def parse_detail(response):

        # 通过 CSS 选择器找出具体值
        title = response.css("h1>span:nth-child(1)::text").extract_first()
        rating = response.css('.rating_num::text').extract_first()
        
        # 实例化对象
        subject_item = MyspiderItem()
        subject_item['title'] = title
        subject_item['douban_link'] = response.url
        subject_item['rating'] = rating

        # 移交 pipeline 流水线 
        yield subject_item