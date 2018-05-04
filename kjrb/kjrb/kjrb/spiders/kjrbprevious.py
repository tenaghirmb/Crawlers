# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from kjrb.items import News
import re


class KjrbpreviousSpider(Spider):
    name = "kjrbprevious"
    allowed_domains = ["digitalpaper.stdaily.com"]
    contenturl = 'content_{newsid}.htm?div=-1'
    start_urls = ['http://digitalpaper.stdaily.com/http_www.kjrb.com/kjrb/html/{year}-{month:02d}/{day:02d}/node_2.htm'.format(year=year, month=month, day=day) for year in range(2012, 2017) for month in range(1, 13) for day in range(1, 32)]

    def parse(self, response):
        pagelist = response.xpath('//a[@id="pageLink"]').extract()
        for page in pagelist:
            temp = re.search('第(.*?)版：(.*?)</a>', page)
            pageNo = temp.group(1)
            pageName = temp.group(2)
            t = response.url.split('/')
            t.pop()
            t.append('node' + re.search('node(.*?)">', page).group(1))
            pageurl = '/'.join(t)
            request = Request(pageurl, self.parse_newslist)
            request.meta['page'] = {'pageNo':pageNo, 'pageName':pageName}
            yield request

    def parse_newslist(self, response):
        newslist = response.xpath('//a/div[@id]').extract()
        pageinfo = response.meta['page']
        for news in newslist:
            newsid = re.search('id="mp(.*?)">', news).group(1)
            t = response.url.split('/')
            t.pop()
            t.append(self.contenturl.format(newsid=newsid))
            newsurl = '/'.join(t)
            request = Request(newsurl, self.parse_news)
            request.meta['page'] = pageinfo
            yield request

    def parse_news(self, response):
        item = News()
        pageinfo = response.meta['page']
        item['url'] = response.url
        item['pageNo'] = pageinfo['pageNo']
        item['pageName'] = pageinfo['pageName']
        biaoti = response.xpath('//div[@class="biaoti"]').extract_first()
        item['biaoti'] = re.search('<div class="biaoti">(.*?)</div>', biaoti).group(1)
        yinti = response.xpath('//div[@class="yinti"]').extract_first()
        item['yinti'] = re.search('<div class="yinti">(.*?)</div>', yinti).group(1)
        futi = response.xpath('//div[@class="futi"]').extract_first()
        item['futi'] = re.search('<div class="futi">(.*?)</div>', futi).group(1)
        author = response.xpath('//div[@class="author"]').extract_first()
        item['author'] = re.search('<div class="author">(.*?)</div>', author).group(1)
        picture = response.xpath('//div[@class="picture"]').extract_first()
        if picture:
            item['picture'] = 'http://digitalpaper.stdaily.com/http_www.kjrb.com/kjrb/'+re.search('<img src="../../../(.*?)">', picture).group(1)
        else:
            item['picture'] = None
        article = response.xpath('//div[@class="article"]').extract_first()
        item['article'] = re.search('<!--enpcontent-->(.*?)<!--/enpcontent-->', article, re.S).group(1)
        yield item