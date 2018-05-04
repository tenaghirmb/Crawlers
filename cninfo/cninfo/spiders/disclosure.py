# -*- coding: utf-8 -*-
from scrapy import Spider, FormRequest
import json
from cninfo.items import CninfoItem


class DisclosureSpider(Spider):
    name = 'disclosure'
    allowed_domains = ['cninfo.com.cn']
    curl = 'http://www.cninfo.com.cn/cninfo-new/disclosure/{column}_latest'
    switcher = {
    'szse_main':'深市主板公告',
    'szse_sme':'深市中小板公告',
    'szse_gem':'深市创业板公告',
    'sse':'沪市公告',
    }

    def start_requests(self):
        for c in self.switcher.keys():
            yield FormRequest(self.curl.format(column=c), formdata={'column':c,'columnTitle':self.switcher.get(c),'pageNum':'1','pageSize':'30','tabName':'latest'}, callback=self.parse_announce, meta={'column':c,'columnTitle':self.switcher.get(c),'page':1})

    def parse_announce(self, response):
        alist = json.loads(response.text)
        if alist['hasMore']:
            yield FormRequest(self.curl.format(column=response.meta['column']), formdata={'column':response.meta['column'],'columnTitle':response.meta['columnTitle'],'pageNum':str(response.meta['page']+1),'pageSize':'30','tabName':'latest'}, callback=self.parse_announce, meta={'column':response.meta['column'],'columnTitle':response.meta['columnTitle'],'page':response.meta['page']+1}, dont_filter=True)
        ca = alist['classifiedAnnouncements']
        for a in ca:
            for result in a:
                item = CninfoItem()
                for field in item.fields:
                    if field in result.keys():
                        item[field] = result.get(field)
                item['pubdate'] = result.get('announcementTime')
                item['file_urls'] = ['http://www.cninfo.com.cn/'+item['adjunctUrl']]
                yield item