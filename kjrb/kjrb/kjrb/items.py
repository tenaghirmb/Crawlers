# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class News(Item):
    url = Field()
    yinti = Field()
    biaoti = Field()
    futi = Field()
    author = Field()
    picture = Field()
    article = Field()
    pageNo = Field()
    pageName = Field()