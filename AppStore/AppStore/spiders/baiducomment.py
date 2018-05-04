# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from AppStore.items import comment
import re

class BaiducommentSpider(Spider):
    name = 'baiducomment'
    allowed_domains = ['baidu.com']
    switcher = {
    '5039112':'E海通财',
    '4703270':'东方财富证券',
    '7072825':'平安证券',
    '7071149':'广发易淘金',
    '7043679':'同花顺',
    '4992266':'国信金太阳',
    '2928831':'智远一户通',
    '4753322':'佣金宝',
    '5037599':'金阳光'
    }
    start_urls = ['http://shouji.baidu.com/comment?action_type=getCommentList&groupid={gid}&pn={p}'.format(gid=gid,p=str(p)) for gid in switcher.keys() for p in range(1,30)]

    def parse(self, response):
        aname = self.switcher.get(re.search('groupid=(.*?)&pn',response.url).group(1))
        try:
            clist = response.xpath('//li[@class="comment"]').extract()
            for c in clist:
                item = comment()
                item['aname'] = aname
                item['store'] = 'baidu'
                item['content'] = re.search('<div><p>(.*?)</p></div>',c).group(1).strip()
                item['ctime'] = re.search('<div class="comment-time">(.*?)</div>',c).group(1).strip()
                yield item
        except:
            pass
