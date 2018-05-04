# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from jwc_ecust.items import News
import re


class DailySpider(CrawlSpider):
    name = "daily"
    allowed_domains = ["jwc.ecust.edu.cn"]
    start_urls = ['http://jwc.ecust.edu.cn/']

    rules=(
            Rule(LinkExtractor(allow=('page\.(htm|psp)',)), callback='parse_news', follow=True),        
    )

    def parse_news(self, response):
        item = News()
        item['url'] = response.url
        item['title'] = response.xpath('//title').extract_first().strip('<title>').strip('</title>')
        author = response.xpath('//span[@class="Article_Publisher"]').extract_first()
        item['author'] = re.search('>(.*?)<', author).group(1)
        date = response.xpath('//span[@class="Article_PublishDate"]').extract_first()
        item['date'] = re.search('>(.*?)<', date).group(1)
        item['content'] = response.xpath('//div[@class="Article_Content"]').extract_first()
        item['alink'] = []
        alinks = response.xpath('//div[@class="Article_Content"]//a').extract()
        for link in alinks:
            try:
                aurl = 'http://jwc.ecust.edu.cn'+re.search('href=\"(.*?)\"', link).group(1)
                atitle = re.search('\>(.*?)\<', link).group(1)
                if not(re.search('mailto', aurl)):
                    item['alink'].append({"aurl":aurl , "atitle":atitle })
                else:
                    pass
            except:
                print("\t\t获取附件出错！")
        yield item
