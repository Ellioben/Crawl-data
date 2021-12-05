# -*- codeing = utf-8 -*-
# @Time : 2021/3/15 16:54
# @File : wordCloudDemo.py
import matplotlib
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3


conn = sqlite3.connect("../video250.db")
c=conn.cursor()
sql = 'select video_name from video250'
data = c.execute(sql)
text = ''
for i in data:
    text = text+i[0]
    #print(text)
conn.commit()
conn.close()
#分词
cut = jieba.cut(text)
string = ' '.join(cut)
print(string)
print(len(string))
#wordcloud
img = Image.open(r"image/erji.png")
img_array = np.array(img)
wordcloud = WordCloud(
    #background_color='white',
    mask = img_array,
    font_path='simhei.ttf'
).generate_from_text(string)

#绘制图片
fig = plt.figure(1)
plt.imshow(wordcloud)
#是否显示坐标轴
plt.axis('off')
#显示生成的词云图片
#plt.show()
#输出词云图片
plt.savefig(r'image\高dpi.jpg',dpi=500)