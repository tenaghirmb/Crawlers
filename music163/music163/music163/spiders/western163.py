# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from music163.items import Artist, Album, Song
import json
import re

class Western163(Spider):
    name = "western163"
    allowed_domains = ["music.163.com", "api.imjad.cn"]
    api = 'https://api.imjad.cn/cloudmusic/?type={type}&id={id}'
    arurl = 'http://music.163.com/artist/album?id={ar_id}&limit=800'
    start_urls = ['http://music.163.com/discover/artist/cat?id={catid}&initial={initial}'.format(catid=str(c), initial=str(i)) for c in range(2001, 2004) for i in list(range(65, 91))+[0]]

    def parse(self, response):
        arlist = response.css('a.nm.nm-icn.f-thide.s-fc0').extract()
        cat = re.search('cat\?id=(.*?)&initial', response.url).group(1)
        for artist in arlist:
            aid = re.search('href="/artist\?id=(.*?)"', artist)
            ar_id = aid.group(1)
            yield Request(self.arurl.format(ar_id=ar_id), self.get_album_id)
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

    def get_album_id(self, response):
        alist = response.css('a.tit.s-fc0').extract()
        for album in alist:
            als = re.search('href="/album\?id=(.*?)"', album)
            al_id = als.group(1)
            yield Request(self.api.format(type='album', id=al_id), self.parse_album)

    def parse_album(self, response):
        albuminfo = json.loads(response.text)
        item = Album()

        for field in item.fields:
            if field in albuminfo['album'].keys():
                item[field] = albuminfo['album'].get(field)
        item['arid'] = albuminfo['album']['artist']['id']
        item['shareCount'] = albuminfo['album']['info']['shareCount']
        item['commentCount'] = albuminfo['album']['info']['commentCount']
        yield item

        slist = albuminfo['songs']
        for song in slist:
            sid = song['id']
            yield Request(self.api.format(type='detail', id=sid), self.parse_song)

    def parse_song(self, response):
        detail = json.loads(response.text)
        item = Song()

        for field in item.fields:
            if field in detail['songs'][0].keys():
                item[field] = detail['songs'][0].get(field)
        item['alid'] = detail['songs'][0]['al']['id']
        request = Request(self.api.format(type='lyric', id=item['id']), self.parse_lyric)
        request.meta['item'] = item
        yield request

    def parse_lyric(self, response):
        lyric = json.loads(response.text)
        item = response.meta['item']

        for field in item.fields:
            if field in lyric.keys():
                item[field] = lyric.get(field)
        request = Request(self.api.format(type='comments', id=item['id']), self.parse_comments)
        request.meta['item'] = item
        yield request

    def parse_comments(self, response):
        comments = json.loads(response.text)
        item = response.meta['item']

        for field in item.fields:
            if field in comments.keys():
                item[field] = comments.get(field)
        
        request = Request(self.api.format(type='comments', id=item['id'])+'&limit='+str(item['total']),self.parse_com)
        request.meta['item'] = item
        yield request

    def parse_com(self, response):
        comments = json.loads(response.text)
        item = response.meta['item']
        item['comments'] = comments['comments']
        yield item