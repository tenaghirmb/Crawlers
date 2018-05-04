# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class News(Item):
    url  = Field()
    title = Field()
    author = Field()
    date = Field()
    content = Field()
    alink = Field()
