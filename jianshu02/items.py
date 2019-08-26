# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Jianshu02Item(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    articleid = scrapy.Field()
    author = scrapy.Field()
    publicdate = scrapy.Field()
    text_num = scrapy.Field()
    read_num = scrapy.Field()
    comment_num = scrapy.Field()
    like_num = scrapy.Field()
    cated = scrapy.Field()
    stars = scrapy.Field()
