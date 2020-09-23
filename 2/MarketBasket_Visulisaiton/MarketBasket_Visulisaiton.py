'''
MarketBasket Analysis

Dataset：MarketBasket
Link：https://www.kaggle.com/dragonheir/basket-optimisation

Visualisation of Top 10 best sell items.

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
# Use WordCloud to visualise data

# Create a WordCloud instance and set parameters
wc = WordCloud(max_words=10, width=2000, height=1000, collocations=False)

# Generate wordcloud
wordcloud = wc.generate(all_word)

# Plot wordcloud
plt.imshow(wordcloud)

# Save picture to file
wordcloud.to_file("wordcloud.jpg")



# -----------------------------------------------
# Sort and select Top 10 best sell items

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


