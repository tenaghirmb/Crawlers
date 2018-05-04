# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from AppStore.items import comment, AppstoreItem
import json
import re
import datetime

class A360commentSpider(Spider):
    name = '360'
    allowed_domains = ['360.cn']
    header = {
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'DNT':'1',
    'Host':'comment.mobilem.360.cn',
    'Pragma':'no-cache'
    }
    idswitcher = {
    'E海通财':'1974098',
    '涨乐':'1706454',
    '国泰君安君弘':'2762078',
    '东方财富证券':'4827',
    '平安证券':'426362',
    '广发易淘金':'2391753',
    '同花顺':'1918',
    '国信金太阳':'3051',
    '银河玖乐':'256958',
    '信e投':'3268469',
    '智远一户通':'3106234',
    '长江e号':'714402',
    '小方':'3187883',
    '佣金宝':'2571920',
    '金阳光':'5138'
    }
    switcher = {
    '%E6%B5%B7%E9%80%9Ae%E6%B5%B7%E9%80%9A%E8%B4%A2+Android_com.android.haitong':'E海通财',
    '%E6%B6%A8%E4%B9%90%E8%B4%A2%E5%AF%8C%E9%80%9A+Android_com.lphtsccft':'涨乐',
    '%E6%98%93%E9%98%B3%E6%8C%87Plus+Android_com.guotai.dazhihui':'国泰君安君弘',
    '%E4%B8%9C%E6%96%B9%E8%B4%A2%E5%AF%8C%E9%80%9A':'东方财富证券',
    '%E5%AE%89e%E7%90%86%E8%B4%A2%E9%AB%98%E7%AB%AF%E7%89%88+Android_com.hundsun.winner.pazq':'平安证券',
    '%E5%B9%BF%E5%8F%91%E8%AF%81%E5%88%B8%E6%98%93%E6%B7%98%E9%87%91+Android_com.gf.client':'广发易淘金',
    '%E5%90%8C%E8%8A%B1%E9%A1%BA(%E7%82%92%E8%82%A1%E5%BF%85%E5%A4%87)+android':'同花顺',
    '%E9%87%91%E5%A4%AA%E9%98%B3':'国信金太阳',
    '%E7%8E%96%E4%B9%90-%E9%93%B6%E6%B2%B3%E8%AF%81%E5%88%B8+Android_com.galaxy.stock':'银河玖乐',
    '%E4%BF%A1E%E6%8A%95+Android_com.zxscnew':'信e投',
    '%E6%99%BA%E8%BF%9C%E7%90%86%E8%B4%A2+Android_com.cmschina.stock':'智远一户通',
    '%E9%95%BF%E6%B1%9Fe%E5%8F%B7+Android_com.eno.android.cj.page':'长江e号',
    '%E5%B0%8F%E6%96%B9II+Android_com.foundersc.app.xf':'小方',
    '%E4%BD%A3%E9%87%91%E5%AE%9D%E4%B8%872%E7%82%B95%E7%82%92%E8%82%A1+Android_cn.com.gjzq.yjb2':'佣金宝',
    '%E9%87%91%E9%98%B3%E5%85%89%E7%A7%BB%E5%8A%A8%E8%AF%81%E5%88%B8':'金阳光'
    }
    infourl = 'http://zhushou.360.cn/detail/index/soft_id/'
    start_urls = ['http://comment.mobilem.360.cn/comment/getComments?baike={baike}&a=getmessage&count=10&start=0'.format(baike=temp) for temp in switcher.keys()]

    def parse(self, response):
        name = self.switcher.get(re.search('baike=(.*?)&a=', response.url).group(1))
        sid = self.idswitcher.get(name)
        rf = self.infourl+sid
        self.header['Referer'] = rf
        ccnt = json.loads(response.text)['data']['total']
        request = Request(rf,self.parse_info)
        request.meta['info'] = {'ccnt':ccnt,'name':name}
        yield request
        for i in range(0,2001,10):
            yield Request(response.url.rstrip('0')+str(i), self.parse_comment, headers=self.header)

    def parse_comment(self, response):
        try:
            clist = json.loads(response.text)['data']['messages']
            aname = self.switcher.get(re.search('baike=(.*?)&a=', response.url).group(1))
            for c in clist:
                item = comment()
                item['aname'] = aname
                item['store'] = '360'
                item['content'] = c['content']
                item['ctime'] = c['create_time']
                yield item
        except:
            pass

    def parse_info(self, response):
        store = '360'
        info = response.meta['info']
        download = response.xpath('//div[@class="pf"]/span[@class="s-3"]/text()').extract_first()
        dtime = re.search('下载：(.*?)万次',download).group(1)
        rate = response.xpath('//span[@class="s-1 js-votepanel"]/text()').extract_first()
        item = AppstoreItem()
        today = datetime.date.today()
        item['name'] = info['name']
        item['dtime'] = int(dtime)
        item['store'] = store
        item['intime'] = str(today)
        item['ccnt'] = info['ccnt']
        item['rate'] = int(float(rate)*10)
        yield item