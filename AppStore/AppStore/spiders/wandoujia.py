# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from AppStore.items import AppstoreItem, comment
import re
import datetime


class WandoujiaSpider(Spider):
    name = 'wandoujia'
    allowed_domains = ['wandoujia.com']
    switcher = {
    'com.android.haitong':'E海通财',
    'com.lphtsccft':'涨乐',
    'com.guotai.dazhihui':'国泰君安君弘',
    'com.eastmoney.android.berlin':'东方财富证券',
    'com.hundsun.winner.pazq':'平安证券',
    'com.gf.client':'广发易淘金',
    'com.hexin.plat.android':'同花顺',
    'com.guosen.android':'国信金太阳',
    'com.galaxy.stock':'银河玖乐',
    'com.zxscnew':'信e投',
    'com.cmschina.stock':'智远一户通',
    'com.eno.android.cj.page':'长江e号',
    'com.foundersc.app.xf':'小方',
    'cn.com.gjzq.yjb2':'佣金宝',
    'com.hundsun.stockwinner.gdzq':'金阳光'
    }
    start_urls = ['http://www.wandoujia.com/apps/{pname}'.format(pname=p) for p in switcher.keys()]

    def parse(self, response):
        store = 'wandoujia'
        pname = response.url.split('/')[-1]
        name = self.switcher.get(pname)
        item = AppstoreItem()
        download = response.xpath('//div[@class="download-wp"]').extract_first()
        dtime = re.search('data-install="(.*?)万"',download).group(1)
        rate = response.xpath('//span[@class="item love"]/i/text()').extract_first().strip('%')
        ccnt = response.xpath('//a[@class="item last comment-open"]/i/text()').extract_first()
        today = datetime.date.today()
        item['name'] = name
        item['dtime'] = float(dtime)
        item['intime'] = str(today)
        item['store'] = store
        item['rate'] = int(float(rate))
        item['ccnt'] = int(ccnt)
        request = Request(response.url+'/comment1', self.parse_page)
        request.meta['info'] = {'aname':name}
        yield request
        yield item

    def parse_page(self, response):
    	info = response.meta['info']
    	try:
    		plist = response.xpath('//div[@class="pagination"]/div/a').extract()
    		p = int(re.search('>(.*?)</a>',plist[-2]).group(1))
    	except IndexError:
    		p = 1
    	for i in range(1,p+1):
    		request = Request(response.url.strip('1')+str(i), self.parse_comment)
    		request.meta['info'] = info
    		yield request

    def parse_comment(self, response):
        info = response.meta['info']
        clist = response.xpath('//ul[@class="comments-list"]/li').extract()
        for c in clist:
            item = comment()
            item['aname'] = info['aname']
            item['store'] = 'wandoujia'
            item['content'] = re.search('<p class="cmt-content"><span>(.*?)</span>',c,re.S).group(1).strip()
            ctime = re.search('<span class="name">(.*?)</span><span>(.*?)</span>',c).group(2).strip()
            item['ctime'] = re.sub('\D','-',ctime).strip('-')
            yield item
