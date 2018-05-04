# -*- coding: utf-8 -*-
from PIL import Image
import jieba
import codecs
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
from wordcloud import WordCloud, ImageColorGenerator

date = "2017-04/07"
client = MongoClient()
db = client.kjrb
cursor = db.news.find({"url":{"$regex": date}})
text = ''
for document in cursor:
	article = document.get('article')
	article = article.strip('</p>')
	article = article.strip()
	article = article.replace('<p>','')
	article = article.replace('</p>','')
	article = article.replace('<strong>','')
	article = article.replace('</strong>','')
	article = article.replace('\n','')
	text = text + article

stopwords = ["我","我们","你","你们","它","它们","他","他们","她","她们","如果","如何","每个","是否","期间","难以","即便","从而","产生","获得","不同","一次","那么","持续","其他","事实上","现有","面对","其他","近日","没有","多年","首次","无法","这里","显示","更加","形成","了解","关于","出现","给予","随着","为了","最近","但是","那些","不能","可以","一些","这个","认为","就是","主要","成为","作为","进行","包括","还是","不是","此次","已经","开始","目前","只有","只要","可能","之间","一个","需要","表示","具有","人们","自己","作用","通过","发现","甚至","以及","一种","同时","情况","能够","由于","不过","这些","正在","其中","相关","直接","进一步","来自","利用","实现","之一","使用","告诉","这种","这样","发生","什么","完成","应该","非常","十分","现在","目前","一条","不断","提供","共同","第一","第二","很多","采用","这一","方面","所有","对于","比如","记者","日电","各种","多个","一样","比如","而是","许多","真正","进入","几乎","只是","按照","根据","不仅","结束","有效","这是","那是","一定","每年","任何","最终","最后","虽然","解决","达到","举行","因此","重要","终于","大家","一直","尽管","对应","得到","以上","完全","带来","自身","科技日报","本报记者"]
cloud_coloring = np.array(Image.open("cloud_mask.jpg"))

wc = WordCloud(font_path='msyh.ttc',background_color="white", max_words=10000, mask=cloud_coloring,
               stopwords=stopwords, max_font_size=42, random_state=42)

temp = jieba.cut(text)
news = ','.join(temp)

# generate word cloud
wc.generate(news)

# create coloring from image
image_colors = ImageColorGenerator(cloud_coloring)

# show
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(cloud_coloring, cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")
plt.show()