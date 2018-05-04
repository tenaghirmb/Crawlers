# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import json
import re


class Lyric163Spider(Spider):
    name = "lyric163"
    allowed_domains = ["music.163.com"]
    albumurl = 'http://music.163.com/album?id={al_id}'
    lyricapi = 'http://music.163.com/api/song/lyric?id={sid}&lv=1'    # 旧版网易云音乐api  https://zhuanlan.zhihu.com/p/21326015
    artistid = '96266'    # 在这里定义要爬取的歌手的id
    start_urls = ['http://music.163.com/artist/album?id={ar_id}&limit=800'.format(ar_id=artistid)]
    def parse(self, response):
    	alist = response.css('a.tit.s-fc0').extract()
    	for album in alist:
            als = re.search('href="/album\?id=(.*?)"', album)
            al_id = als.group(1)
            yield Request(self.albumurl.format(al_id=al_id), self.parse_album)

    def parse_album(self, response):
        slist = response.xpath('//ul[@class="f-hide"]/li/a[@href]').extract()
        
        for song in slist:
            sid = re.search('href="/song\?id=(.*?)">', song).group(1)
            yield Request(self.lyricapi.format(sid=sid), self.parse_lyric)

    def parse_lyric(self, response):
    	res = json.loads(response.text)
    	lrc = res.get('lrc')['lyric']
    	lrc = re.sub('\[.*?\]','',lrc)
    	lrc = re.sub('作曲.*?\n','',lrc)
    	lrc = re.sub('作词.*?\n','',lrc)
    	with open('C:\\Users\\TENAG\\Documents\\GitHub\\music163\\lyric.txt','a') as f:
    		f.write(lrc)
    		print('写入成功')