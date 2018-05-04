# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Artist(Item):
    # from api --artist['artist'].keys()--
    name = Field()          # 歌手名字
    id = Field()            # 歌手id
    picUrl = Field()        # 歌手主页封面
    briefDesc = Field()     # 歌手简介
    albumSize = Field()     # 专辑数
    musicSize = Field()     # 歌曲数
    mvSize = Field()        # MV数
    transNames = Field()    # 翻译名
    cat = Field()           # 歌手分类 --2001：欧美男歌手； 2002：欧美女歌手； 2003：欧美组合/乐队--


class Album(Item):
    # --album['album']['artist']['id']--
    arid = Field()          # 歌手id
    # --album['album'].keys()--
    name = Field()          # 专辑名
    id = Field()            # 专辑id
    blurPicUrl = Field()    # 专辑封面
    company = Field()       # 唱片公司
    description = Field()   # 专辑简介
    size = Field()          # 专辑歌曲数量
    type = Field()          # 专辑类型
    subType = Field()       # 专辑细分类别
    # --album['album']['info'].keys()--
    shareCount = Field()    # 分享次数
    commentCount = Field()  # 评论数


class Song(Item):
    # --detail['songs'][0]['al']['id']--
    alid = Field()          # 专辑id
    # --detail['songs'][0].keys()--
    name = Field()          # 歌名
    id = Field()            # 歌曲id
    ar = Field()            # 演唱的所有歌手
    no = Field()            # 歌曲编号
    pop = Field()           # 歌曲热度
    mv = Field()            # MV数量

    # --lyric.keys()--
    lrc = Field()           # 歌词
    tlyric = Field()        # 翻译歌词

    # --comments.keys()--
    hotComments = Field()   # 热评
    total = Field()         # 评论数
    
    # 获取评论数后设置url的limit参数获取所有评论
    comments = Field()      # 所有评论