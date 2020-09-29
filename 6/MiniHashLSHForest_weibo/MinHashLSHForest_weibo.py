'''
使用MinHashLSHForest对微博新闻句子进行检索 weibo.txt
针对某句话进行Query，查找Top-3相似的句子

1、完成代码（30points）
2、使用MinHashLSHForest工具对MinHash进行index，并完成Query Top-K，代码正确（30points）

'''

from datasketch import MinHash, MinHashLSH, MinHashLSHForest
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba.posseg as pseg
import re


# 读取文件
f = open('./weibos.txt', 'r', encoding='UTF-8')
text = f.read()
# 以句号，叹号，问号作为分隔，去掉\n换行符号
sentences = re.split('[。！？]', text.replace('\n', ''))

# 最后一行如果为空，则删除
if sentences[len(sentences)-1] == '':
    sentences.pop()
#print(sentences)
#print(len(sentences))

# 将item_text进行分词
def get_item_str(item_text):
    item_str = "" 
    item=(pseg.cut(item_text)) 
    for i in list(item):
        #去掉停用词
        if i.word not in list(stop):  
            item_str += i.word
            #tfidf_vectorizer.fit_transform的输入需要空格分隔的单词
            item_str += " "
    return item_str
# 对item_str创建MinHash
def get_minhash(item_str):
    temp = MinHash()
    for d in item_str:
        temp.update(d.encode('utf8'))
    return temp

# 设置停用词
stop = [line.strip() for line in open('stopword.txt').readlines()]
#stop = [line.strip().decode('utf-8') for line in open('stopword.txt').readlines()]
# 得到分词后的documents
documents = []
for item_text in sentences:
    # 将item_text进行分词
    item_str = get_item_str(item_text)
    documents.append(item_str)

# 创建LSH Forest及MinHash对象
minhash_list = []
forest = MinHashLSHForest()
for i in range(len(documents)):
    #得到train_documents[i]的MinHash
    temp = get_minhash(documents[i])
    minhash_list.append(temp)
    forest.add(i, temp)
# index所有key，以便可以进行检索
forest.index()

query = '国足输给叙利亚后，里皮坐不住了'
# 将item_text进行分词
item_str = get_item_str(query)
# 得到item_str的MinHash
minhash_query = get_minhash(item_str)

# 查询forest中与m1相似的Top-K个邻居
result = forest.query(minhash_query, 3)
for i in range(len(result)):
    print(result[i], minhash_query.jaccard(minhash_list[result[i]]), documents[result[i]].replace(' ', ''))
print("Top 3 邻居", result)


'''
运行结果

1 0.6015625 ​国足输给叙利亚之后里皮辞职
29 0.2734375 ​带队绝不会比里皮更差​一定能带国足夺得2022世界杯冠军
37 0.40625 国足昨晚-输给叙利亚赛后主帅里皮宣布辞职
Top 3 邻居 [1, 29, 37]

'''