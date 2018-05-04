# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import json
import codecs
import re

class LyricleanSpider(Spider):
    name = "lyriclean"
    allowed_domains = ["music.163.com"]
    lyricapi = 'http://music.163.com/api/song/lyric?id={sid}&lv=1'    # 旧版网易云音乐api  https://zhuanlan.zhihu.com/p/21326015
    start_urls = ['http://music.163.com/album?id={al_id}'.format(al_id=id) for id in ['1963864','421969','421935','1963861','1963859','1963855','3152321','34908195','35186017']]

    def parse(self, response):
        slist = response.xpath('//ul[@class="f-hide"]/li/a[@href]').extract()
        
        for song in slist:
            sid = re.search('href="/song\?id=(.*?)">', song).group(1)
            if re.search('Remix', song):
            	pass
            else:
            	yield Request(self.lyricapi.format(sid=sid), self.parse_lyric)

    def parse_lyric(self, response):
    	res = json.loads(response.text)
    	lrc = res.get('lrc')['lyric']
    	lrc = re.sub('\[.*?\]',' ',lrc)
    	lrc = re.sub('作曲.*?\n',' ',lrc)
    	lrc = re.sub('作词.*?\n',' ',lrc)
    	with codecs.open('C:\\Users\\TENAG\\Documents\\GitHub\\music163\\M5 wordcloud\\lyric.txt','a','utf-8') as f:
    		f.write(lrc)
    		print('写入成功')