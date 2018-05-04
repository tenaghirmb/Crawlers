from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import codecs
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Read the whole text.
with codecs.open("lyric.txt",'r','utf-8') as f:
	text = f.read()

maroon_coloring = np.array(Image.open("mask.jpg"))
stopwords = set(STOPWORDS)
stopwords.add("Maroon 5")

wc = WordCloud(background_color="white", max_words=60000, mask=maroon_coloring, scale=25,
               stopwords=stopwords, max_font_size=40, random_state=42)
# generate word cloud
wc.generate(text)

# create coloring from image
image_colors = ImageColorGenerator(maroon_coloring)

# show
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(maroon_coloring, cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")
plt.show()