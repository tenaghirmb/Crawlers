# -*- coding: utf-8 -*-
import pymongo
import datetime

class MongoPipeline(object):

    collection_name = 'disclosure'

    def __init__(self, mongo_uri, mongo_db, username, password):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.username = username
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            username=crawler.settings.get('USERNAME'),
            password=crawler.settings.get('PASSWORD')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db.authenticate(self.username,self.password)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item['pubdate'] = str(datetime.datetime.fromtimestamp(float(item['pubdate']/1000)))
        item['storageTime'] = str(datetime.datetime.fromtimestamp(float(item['storageTime']/1000)))
        item['entrytime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db[self.collection_name].update({'adjunctUrl':item['adjunctUrl']},dict(item),True)
        return item