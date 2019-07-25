# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YahooStockNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    code = scrapy.Field()
    company = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()

class BooksItems(scrapy.Item):
    type = scrapy.Field()
    rank = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    # discount = scrapy.Field()
    # price = scrapy.Field()


