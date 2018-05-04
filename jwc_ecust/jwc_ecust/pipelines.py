# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class JwcEcustPipeline(object):
    collection_name = 'news'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            result = self.db[self.collection_name].update_one({"url": item['url']},{"$set":{"title": item['title'], "author": item['author'], "date": item['date'], "content": item['content'], "alink": item['alink']}}, True)
            if result.matched_count==1:
                print('\t'+item['title']+'更新成功')
            else:
                print(item['title']+'入库成功')
        except:
            print('\t\t\t\t********ERROR:'+item['title']+ '入库出错')
        return item
