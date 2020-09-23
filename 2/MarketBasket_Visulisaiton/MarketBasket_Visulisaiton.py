'''
# ---------------------------------------------------------------------------------
 
# Thinking 1, MVC框架指的是什么? 能简要说出MVC框架的内容（20points）

答： MVC框架指Model模型, View视窗, Controller控制器的缩写，一种软件设计典范，
    用一种业务逻辑、数据、界面显示分离的方法组织代码，将业务逻辑聚集到一个部件里面，
    在改进和个性化定制界面及用户交互的同时，不需要重新编写业务逻辑。
    MVC被独特的发展起来用于映射传统的A 输入，处理，输出 三个功能于一个逻辑的图形化用户界面的结构中。

    MVC分层有助于管理复杂的应用程序，让开发人员可以在一个时间内，专注于一个层面，
    可以在不依赖业务逻辑的情况下，专注于试图设计，同时，也让应用程序的测试更加容易。

# ---------------------------------------------------------------------------------

Thinking 2, 基于Python的可视化技术都有哪些，你使用过哪些？分享自己使用过的工具（20points）

答： 基于Python的可视化工具，主要是Matplotlib和seaborn。

    可以用以上两种或其中一种来做以下的可视化图像：
    散点图，常用于了解数据分布情况
    折线图，常用于以时间为其中一个维度的关系
    条形图，常用于对比同一个维度下的互相比较关系
    箱线图，可以表示上届下届，离群值和中位数
    饼图，展现成分构成比例
    热力图，展现多个维度对两两关系强度
    
    另外还有以下需要自己编写代码实现的图形：
    蜘蛛图，展现多维向量
    二元变量分布图，成对关系

    subplot也可用于多个子图的展示。

    我用过散点图，折线图，条形图，饼图和热力图。

# ---------------------------------------------------------------------------------

Action1	"购物篮词云分析

数据集：MarketBasket
下载地址：https://www.kaggle.com/dragonheir/basket-optimisation

对数据集进行词云可视化展示，可视化探索（Top10的商品有哪些）

1、完成可视化的呈现（30points）
2、能分析出TOP10商品并进行可视化呈现（30points）"

'''

from wordcloud import WordCloud
import pandas as pd 
import matplotlib.pyplot as plt 
from PIL import Image
import numpy as np 
from lxml import etree
from nltk.tokenize import word_tokenize
import seaborn as sns
# Chinese charator can use jieba
# import jieba
# jieba.cut()

df = pd.read_csv('Market_Basket_Optimisation.csv', header=None, keep_default_na=False)

# Store each word in transaction
transactions = []

# Calculate and store counts of each word 
item_count = {}

for i in range(0, df.shape[0]):
    for j in range(20):
        item  = str(df.values[i,j])
        if item != 'nan' and item != '':
            # Replace space with under score line
            item = item.lstrip()
            item = item.rstrip()
            item = item.replace(" ", '_')
            # Count this item
            if item not in item_count:
                item_count[item] = 1
            else:
                item_count[item] += 1
            transactions.append(item)

# join all items together, separated by " "
all_word  = " ".join(x for x in transactions)

# -----------------------------------------------
# 1、完成词云可视化的呈现

# Create a WordCloud instance and set parameters
wc = WordCloud(max_words=10, width=2000, height=1000, collocations=False)

# Generate wordcloud
wordcloud = wc.generate(all_word)

# Plot wordcloud
plt.imshow(wordcloud)

# Save picture to file
wordcloud.to_file("wordcloud.jpg")



# -----------------------------------------------
# 2、能分析出TOP10商品并进行可视化呈现

# Sort items by count
df = pd.DataFrame(transactions)
df.columns  =  ['item']
counts = df['item'].value_counts()

x = []
y = []
# Store top 10 item name and it's count in x, y
for i in range(0,10):
    x.append(str(counts.index[i]))
    y.append(int(counts[i]))
    i += 1

# Plot bar chart
plt.bar(x,y, label='Counts')
# Set rotation of x
plt.xticks(rotation=90)

# Show figure on top of each bar
for a, b in zip(x, y):
    plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=10)

plt.legend()
plt.show()


