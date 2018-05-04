# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from AppStore.items import AppstoreItem, comment
import re
import json
import datetime


class MyappSpider(Spider):
    name = 'myapp'
    allowed_domains = ['android.myapp.com']
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
    header = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'DNT':'1',
    'Host':'android.myapp.com',
    'Origin':'http://android.myapp.com',
    'Pragma':'no-cache',
    'Referer':'',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest',
    }
    start_urls = ['http://android.myapp.com/myapp/detail.htm?apkName={apkname}'.format(apkname=k) for k in switcher.keys()]
    curl = 'http://android.myapp.com/myapp/app/comment.htm?apkName={apkname}&apkCode={apkCode}&contextData={contextData}'

    def parse(self, response):
        store = 'myapp'
        js = response.xpath('//script[@type="text/javascript"]').extract()[-1]
        dtime = re.search('downTimes:"(.*?)"',js).group(1)
        rate = response.xpath('//div[@class="com-blue-star-num"]/text()').extract_first().strip('分')
        apkname = re.search('apkName=(.*)',response.url).group(1)
        apkCode = re.search('apkCode : "(.*?)"',js).group(1)
        name = self.switcher.get(apkname)
        self.header['Referer'] = response.url
        requestinfo = Request(self.curl.format(apkname=apkname,apkCode=apkCode,contextData=''), self.parse_info,headers=self.header)
        requestinfo.meta['info'] = {'name':name,'store':store,'dtime':dtime,'rate':rate}
        yield requestinfo

    def parse_info(self, response):
        info = response.meta['info']
        tmp = json.loads(response.text)
        try:
            ccnt = int(tmp['obj']['total'])
        except:
            ccnt = None
        item = AppstoreItem()
        today = datetime.date.today()
        item['name'] = info['name']
        item['dtime'] = int(info['dtime'])
        item['intime'] = str(today)
        item['store'] = info['store']
        item['rate'] = int(float(info['rate'])*10)
        item['ccnt'] = ccnt
        yield item