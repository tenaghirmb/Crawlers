# -*- coding: utf-8 -*-
import json
import datetime
from kafka import KafkaProducer
from AppStore.items import AppstoreItem

class KafkaPipeline(object):


    def __init__(self, producer, topic1,topic2):

        self.producer = producer
        self.topic1 = topic1
        self.topic2 = topic2
        self.today = str(datetime.date.today())


    def process_item(self, item, spider):
        if isinstance(item, AppstoreItem) and item['store'] in ['oppo','wandoujia','baidu','360']:
            item['dtime'] = int(item['dtime']*10000)
        if isinstance(item, AppstoreItem):
            item = dict(item)
            msg = json.dumps(item,ensure_ascii=False,sort_keys=True).encode('utf-8')
            self.producer.send(self.topic1, msg)
        elif item['ctime'][:10]==self.today:
            pass
        else:
            item = dict(item)
            msg = json.dumps(item,ensure_ascii=False,sort_keys=True).encode('utf-8')
            self.producer.send(self.topic2, msg)

    @classmethod
    def from_crawler(cls, crawler):
        k_hosts = crawler.settings.get('SCRAPY_KAFKA_HOSTS')
        topic1 = crawler.settings.get('SCRAPY_KAFKA_ITEM_PIPELINE_TOPIC1')
        topic2 = crawler.settings.get('SCRAPY_KAFKA_ITEM_PIPELINE_TOPIC2')
        conn = KafkaProducer(bootstrap_servers=k_hosts)
        return cls(conn, topic1, topic2)