# -*- coding: utf-8 -*-

from scrapy import Item, Field


class AppstoreItem(Item):
	name = Field()		# 应用名称
	dtime = Field()		# 下载量
	store = Field()		# 应用商店
	intime = Field()	# 入列时间
	ccnt = Field()		# 评论数
	rate = Field()		# 评分


class comment(Item):
	aname = Field()		# 应用名称
	store = Field()		# 应用商店
	ctime = Field()		# 评论时间
	content = Field()	# 评论内容