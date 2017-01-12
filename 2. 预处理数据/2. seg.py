#! /usr/bin/python
import re
import time
import jieba
import string
import jieba.posseg
jieba.enable_parallel()

# 读入停用词
with open("../data/stopwords.txt") as f:
    stopwords = set([i.strip() for i in f.readlines()])
print(len(stopwords))

def seg(content):
    # 去除 url
    content = re.sub(
            r'(?:(?:http|ftp)s?://)?' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:\S*)', "", content, flags=re.MULTILINE | re.IGNORECASE)
    # 去除标点
    ch_punc = "。？！，、；：“”‘’「」『』（）【】〔〕〔〕——……—-～·《》〈〉﹏___"
    content = content.translate(str.maketrans("", "", string.punctuation + ch_punc))
    
    # 分词
    lst = []
    for word in jieba.cut(content):
        if word not in stopwords:
            lst.append(word)
    content = " ".join(lst)
    
    content = re.sub("^ +", "", content, flags=re.MULTILINE)
    content = re.sub(" *\t *", "\t", content)
    content = re.sub("\t+", "\t", content)
    content = re.sub(" +\n", "\n", content)
    content = re.sub(" +", " ", content)
    return content

t1 = time.time()
#with open("../data/train.dat", "rb") as fin, open("../data/train.seg", "wb") as fout:
with open("../../entity/data.in", "rb") as fin, open("../../entity/data.seg", "wb") as fout:
    content = fin.read().decode('utf-8')
    # 去除首行标示
    content = re.sub("^[0-9A-F]+\t[0-6]\t[0-2]\t[0-6]\t", "", content, flags=re.MULTILINE)
    content = seg(content)
    fout.write(content.encode('utf-8'))
""" 
with open("../data/test.dat", "rb") as fin, open("../data/test.seg", "wb") as fout:
    content = fin.read().decode('utf-8')
    # 去除首行标示
    content = re.sub("^[0-9A-F]+\t", "", content, flags=re.MULTILINE)
    content = seg(content)
    fout.write(content.encode('utf-8'))
"""
print(time.time() - t1)
