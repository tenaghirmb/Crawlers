# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from AppStore.items import AppstoreItem, comment
import re
import datetime
from math import ceil

class HuaweiSpider(Spider):
    name = 'huawei'
    allowed_domains = ['app.hicloud.com','appstore.huawei.com']
    switcher = {
    'C10278608':'E海通财',
    'C10156056':'涨乐',
    'C10401368':'国泰君安君弘',
    'C27936':'东方财富证券',
    'C10308911':'平安证券',
    'C10216954':'广发易淘金',
    'C2861':'同花顺',
    'C10158647':'国信金太阳',
    'C10348839':'银河玖乐',
    'C10515140':'信e投',
    'C10371558':'智远一户通',
    'C10268146':'长江e号',
    'C10454805':'小方',
    'C10239514':'佣金宝',
    'C10390489':'金阳光'
    }
    start_urls = ['http://appstore.huawei.com/app/{sid}'.format(sid=t) for t in switcher.keys()]
    curl = 'http://appstore.huawei.com/comment/commentAction.action?appId={appid}&_page={pno}'

    def parse(self, response):
        store = 'huawei'
        sid = response.url.split('/')[-1]
        name = self.switcher.get(sid)
        item = AppstoreItem()
        rate = response.xpath('//ul[@class="app-info-ul nofloat"]/li/p').extract()[1]
        rate = re.search('class="score_(.*?)"',rate).group(1)
        ccnt = response.xpath('//h4[@class="sub nofloat"]/span[@class="title"]/text()').extract_first().strip()
        ccnt = int(re.search('（(.*?)条',ccnt).group(1))
        download = response.xpath('//span[@class="grey sub"]').extract_first()
        dtime = re.search('下载：(.*?)次', download).group(1)
        today = datetime.date.today()
        item['name'] = name
        item['dtime'] = int(dtime)
        item['store'] = store
        item['intime'] = str(today)
        item['rate'] = int(rate)
        item['ccnt'] = ccnt
        yield item
        p = ceil(ccnt/5)
        for i in range(1,p+2):
            request = Request(self.curl.format(appid=sid, pno=str(i)), self.parse_comment)
            request.meta['info'] = {'aname':name,'store':store}
            yield request

    def parse_comment(self, response):
    	info = response.meta['info']
    	clist = response.xpath('//div[@class="comment"]').extract()
    	for c in clist:
    		item = comment()
    		item['aname'] = info['aname']
    		item['store'] = info['store']
    		item['content'] = re.search('<p class="content">(.*?)</p>',c,re.S).group(1).strip()
    		item['ctime'] = re.search('<span class="frt">(.*?)</span>',c).group(1)
    		yield item