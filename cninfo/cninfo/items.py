# -*- coding: utf-8 -*-

from scrapy import Item, Field


class CninfoItem(Item):
	adjunctSize = Field()			# 文件大小
	adjunctUrl = Field()			# 文件地址
	pubdate = Field()				# 发布时间
	announcementTitle = Field()		# 公告标题
	announcementTypeName = Field()	# 公告类别
	secCode = Field()				# 股票代码
	secName = Field()				# 股票名称
	storageTime = Field()			# 收录时间
	entrytime = Field()				# 入库时间
	files = Field()
	file_urls = Field()