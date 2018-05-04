# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from AppStore.items import AppstoreItem, comment
import re
import datetime
import json

class OppoSpider(Spider):
    name = 'oppo'
    allowed_domains = ['oppomobile.com']
    switcher = {
    '11/059/976':'E海通财',
    '20/006/939':'涨乐',
    '11/064/372':'国泰君安君弘',
    '11/019/022':'东方财富证券',
    '11/069/947':'平安证券',
    '20/000/972':'广发易淘金',
    '11/072/067':'同花顺',
    '11/044/742':'国信金太阳',
    '20/001/317':'智远一户通',
    '10/941/723':'长江e号',
    '20/002/134':'小方',
    '10/948/757':'佣金宝',
    '10/981/827':'金阳光'
    }
    start_urls = ['http://store.oppomobile.com/product/00{sid}.html'.format(sid=s) for s in switcher.keys()]
    curl = 'http://store.oppomobile.com/comment/list.json?id={aid}&page={p}'

    def parse(self, response):
        store = 'oppo'
        sid = re.search('/00(.*?).html',response.url).group(1)
        aid = re.sub('/','',sid)
        name = self.switcher.get(sid)
        rate = response.xpath('//div[@class="soft_info_nums"]/div/@class').extract_first().strip('star_')
        download = response.xpath('//div[@class="soft_info_nums"]').extract_first()
        download = re.search('</a>(.*?)次下载',download,re.S).group(1).strip()
        dtime = re.search('^(.*?)万',download).group(1)
        request = Request(self.curl.format(aid=aid,p='1'), self.parse_page)
        request.meta['info'] = {'aname':name,'aid':aid,'dtime':dtime,'rate':rate}
        yield request

    def parse_page(self, response):
        info = response.meta['info']
        temp = json.loads(response.text)
        item = AppstoreItem()
        ccnt = temp['totalNum']
        today = datetime.date.today()
        item['name'] = info['aname']
        item['dtime'] = int(info['dtime'])
        item['intime'] = str(today)
        item['store'] = 'oppo'
        item['rate'] = int(info['rate'])
        item['ccnt'] = int(ccnt)
        yield item
        totalPage = int(temp['totalPage'])
        for i in range(1,totalPage+1):
            request = Request(self.curl.format(aid=info['aid'], p=str(i)), self.parse_comment)
            request.meta['info'] = info
            yield request

    def parse_comment(self, response):
        info = response.meta['info']
        temp = json.loads(response.text)
        clist = temp['commentsList']
        for c in clist:
            item = comment()
            item['aname'] = info['aname']
            item['store'] = 'oppo'
            item['content'] = c['word']
            item['ctime'] = re.sub('\.','-',c['createDate'])
            yield item