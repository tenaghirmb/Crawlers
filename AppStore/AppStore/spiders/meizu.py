# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from AppStore.items import AppstoreItem, comment
from html.parser import HTMLParser
import re
import datetime
import json

class MeizuSpider(Spider):
    name = 'meizu'
    allowed_domains = ['meizu.com']
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
    start_urls = ['http://app.meizu.com/apps/public/detail?package_name={pname}'.format(pname=p) for p in switcher.keys()]
    curl = 'http://app.meizu.com/apps/public/evaluate/list?app_id={appid}&start=0&max=100000'

    def parse(self, response):
        store = 'meizu'
        pname = response.url.split('=')[-1]
        name = self.switcher.get(pname)
        rate = response.xpath('//div[@class="app_content"]/div/@data-num').extract_first()
        dtime = response.xpath('//div[@class="app_content"]/span/text()').extract_first()
        appid = response.xpath('//div[@id="wrapper"]/input').extract_first()
        appid = re.search('data-appid="(.*?)">',appid).group(1)
        request = Request(self.curl.format(appid=appid), self.parse_comment)
        request.meta['info'] = {'aname':name,'dtime':dtime,'rate':rate}
        yield request

    def parse_comment(self, response):
        info = response.meta['info']
        tmp = json.loads(response.text)
        ccnt = tmp['value']['totalCount']
        appitem = AppstoreItem()
        today = datetime.date.today()
        appitem['name'] = info['aname']
        appitem['dtime'] = int(info['dtime'])
        appitem['intime'] = str(today)
        appitem['store'] = 'meizu'
        appitem['rate'] = int(info['rate'])
        appitem['ccnt'] = int(ccnt)
        yield appitem
        clist = tmp['value']['list']
        for c in clist:
            item = comment()
            item['aname'] = info['aname']
            item['store'] = 'meizu'
            item['content'] = HTMLParser().unescape(c['comment'])
            item['ctime'] = c['create_time']
            yield item
