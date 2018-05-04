# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
import pymongo
import logging

class KjrbPipeline(object):
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
            if self.db[self.collection_name].find_one({'url': item['url']}):
                pass
            else:
                self.db[self.collection_name].insert(dict(item))
                logging.log(logging.WARNING, "There's a fresh news coming in "+item['url'][60:-7])
        except:
            logging.log(logging.ERROR, "News "+item['url'][60:-7]+" didn't make it")
        return item

 
class SQLStorePipeline(object):
 
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='baoxinyu',db='kjrb', charset='utf8')
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()
 
    def process_item(self, item, spider):
        self.cursor.execute("select * from kjrb where url = %s", (item['url'], ))
        result = self.cursor.fetchone()
        if result:
            pass
        else:
            self.cursor.execute("insert into kjrb (url, yinti, biaoti, futi, author, picture, article, pageNo, pageName) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (item['url'], item['yinti'], item['biaoti'], item['futi'], item['author'], item['picture'],item['article'], item['pageNo'], item['pageName']))
            self.conn.commit()