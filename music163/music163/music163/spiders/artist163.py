# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from music163.items import Artist
import json
import re


class Artist163Spider(Spider):
    name = "artist163"
    allowed_domains = ["music.163.com", "api.imjad.cn"]
    api = 'https://api.imjad.cn/cloudmusic/?type={type}&id={id}'
    start_urls = ['http://music.163.com/discover/artist/cat?id={catid}&initial={initial}'.format(catid=str(c), initial=str(i)) for c in range(2001, 2004) for i in list(range(65, 91))+[0]]

    def parse(self, response):
    	arlist = response.css('a.nm.nm-icn.f-thide.s-fc0').extract()
    	cat = re.search('cat\?id=(.*?)&initial', response.url).group(1)
    	for artist in arlist:
    		aid = re.search('href="/artist\?id=(.*?)"', artist)
    		ar_id = aid.group(1)
    		request = Request(self.api.format(type='artist', id=ar_id), self.parse_artist)
    		request.meta['item'] = cat
    		yield request

    def parse_artist(self, response):
    	artistinfo = json.loads(response.text)
    	item = Artist()

    	for field in item.fields:
    		if field in artistinfo['artist'].keys():
    			item[field] = artistinfo['artist'].get(field)
    	item['cat'] = response.meta['item']
    	yield item