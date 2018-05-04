# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from AppStore.items import AppstoreItem
import re
import datetime


class BaiduSpider(Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    switcher = {
    '11848584':'E海通财',
    '21946861':'涨乐',
    '21969540':'国泰君安君弘',
    '11192808':'东方财富证券',
    '21935561':'平安证券',
    '21928962':'广发易淘金',
    '21875914':'同花顺',
    '11749715':'国信金太阳',
    '21828019':'信e投',
    '7537915':'智远一户通',
    '21945870':'长江e号',
    '21931589':'小方',
    '11287344':'佣金宝',
    '11842602':'金阳光'
    }
    start_urls = ['http://shouji.baidu.com/software/{sid}.html'.format(sid=t) for t in switcher.keys()]

    def parse(self, response):
        store = 'baidu'
        sid = response.url.split('/')[-1].strip('.html')
        name = self.switcher.get(sid)
        item = AppstoreItem()
        rate = response.xpath('//span[@class="star-percent"]/@style').extract_first()
        rate = re.search('width:(.*?)%',rate).group(1)
        download = response.xpath('//span[@class="download-num"]').extract_first()
        dtime = re.search('下载次数:(.*?)万',download).group(1).strip()
        today = datetime.date.today()
        item['name'] = name
        item['dtime'] = int(dtime)
        item['store'] = store
        item['intime'] = str(today)
        item['rate'] = int(rate)
        item['ccnt'] = 0
        yield item
