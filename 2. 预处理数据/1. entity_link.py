# !/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
from scipy.stats import multivariate_normal
from sklearn.mixture import GMM
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib as mpl
#import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression 
import random
import math
import sys
import re
import ast
import pysolr
import string

class Entity():
    
    entity_title = []
    entity_link = []
    entity_content = []
    
    def content_deal(self, content):
        """
        将输入的content进行处理，删除标点符号、特殊字符等
        按照字符串形式返回
        """
        # 去除 url
        
    
        # 好像直接修改content就可以了
        return content
    
    def content_seg(self, content):
        print(re.sub(r'(?:(?:http|ftp)s?://)?'
                     r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                     r'localhost|'
                     r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                     r'(?::\d+)?'
                     r'(?:\S*)',"","你好 songjs http://dsa.com你好 ,https://localhost"))
        """
        content = re.sub(
                r'(?:(?:http|ftp)s?://)?' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:\S*)', "", content, flags=re.MULTILINE | re.IGNORECASE)
        """
        # 去除标点
        ch_punc = "。？！，、；：“”‘’「」『』（）【】〔〕〔〕——……—-～·《》〈〉﹏___"
        content = content.translate(str.maketrans("", "", string.punctuation + ch_punc))
        
        # 分词
        """
        lst = []
        for word in jieba.cut(content):
            if word not in stopwords:
                lst.append(word)
        content = " ".join(lst)
        """    
        content = re.sub("^ +", "", content, flags=re.MULTILINE)
        content = re.sub(" *\t *", "\t", content)
        content = re.sub("\t+", "\t", content)
        content = re.sub(" +\n", "\n", content)
        content = re.sub(" +", " ", content)
        return content
        
    def __init__(self):
        """
        预处理数据，将数据分别保存到title & content；
        注意需要对content中的标点等进行处理
        """
        """
        with open('./new_abstracts.datab') as f:
            self.data = f.readlines()
        self.title = [] * len(self.data)
        self.content = [] * len(self.data)
            
        pattern_title = re.compile(r'/[\w_.]*>')
        pattern_link = re.compile(r'<[\w_.:/]*>')
        pattern_content = re.compile(r'".*"')
#        pattern_rm = re.compile(r'[,]')
        for i in range(len(self.data)):
            
            
            title = ""
            link = ""
            title = re.findall(pattern_title, self.data[i])
            if(len(title)!=2):
                print("Error col:" + str(i))
            title = ((str)(title[0]))[1:-1]
            num = 0
            for i in range(len(title)):
                if title[i]=='_':
                    num = num+1
            if(num>=3):
                continue

            self.entity_title.append(title)

            link = re.findall(pattern_link, self.data[i])
            link = ((str)(link[0]))[1:-1]
#            print(link)
            self.entity_link.append(link)
            
#            print(self.data[i])
            content = re.findall(pattern_content, self.data[i])
            content = (str)(content)
#            content = self.content_seg(content)
            print(content)
#            content = ((str)(content))[3:-3]

            # 使用正则对content中的标点等进行删除
            # 比如：1993\xe2\x80\x9394 NBA，需要处理
#            content = re.sub(r'.*+"', "", content)
            # 同时删除一些稀有词，因为这里数据量有点大。——删除很长的词汇
            
            self.entity_content.append(content)

        self.entity_title = np.array(self.entity_title)
        self.entity_content = np.array(self.entity_content)
        
        
        
        # 分别将title和content写入文件
        # title用来建立索引，检索使用； content用来获取对应title的主题分布向量
        with open('./in.title_link.dat','w') as f:
            num = (str)(self.entity_title.shape[0])
            print("title col: " + num)
            f.write(num + '\n')
            for i in range(self.entity_title.shape[0]):
 #               print(self.entity_content[i])
                f.write(self.entity_title[i] + ' ' + self.entity_link[i] + '\n')
                
        with open('./in.content.dat','w') as f:
            num = (str)(self.entity_content.shape[0])
            print("content col: " + num)
            f.write(num + '\n')
            for i in range(self.entity_content.shape[0]):
 #               print(self.entity_content[i])
                f.write(self.entity_content[i] + '\n')
        """
        
#        with open('./new_abstracts.datab') as f:
#		with open("../../entity/long_abstracts_en.ttl", "rb") as fin, open("../../entity/data.seg", "wb") as fout:
        with open('../../entity/long_abstracts_en.ttl') as f:            
            self.data = f.readlines()
        pattern_title = re.compile(r'/[\w_.]*>')
        num = 0
        tot = 0
        with open('../../entity/data.in','w') as f:
            for i in range(len(self.data)):
                title = ""
                title = re.findall(pattern_title, self.data[i])
                if(len(title)!=2):
                    num = num+1
                    continue  # 表示没有匹配上
                    
                t = 0
                for j in range(len(title)):
                    if title[j]=='_':
                        t = t+1
                if(t>=3):
                    continue  # 匹配上了，但是title太长，不要
                    
                num = num+1
                if num%100==0:
                    f.write(self.data[i])
                    tot = tot + 1
            print (tot)
            
            
        
    def static(self):
        """
        整合每个entity的主题分布，同时统计每个单词的主题分布
        a) search_entity.dat：保存每个entity & link & 主题分布
        b) search_word.dat：保存每个单词 & 主题分布
        """
        # 读取每个单词映射
        with open('./GibbsLDA++-0.2/models/entity/wordmap.txt') as f:
            wordmap = f.readlines()
        with open('./GibbsLDA++-0.2/models/entity/model-final.tassign') as f:
            tassign = f.readlines()
        with open('./GibbsLDA++-0.2/models/entity/model-final.theta') as f:
            theta = f.readlines()
        
        """
        生成文件：
        search_entity.dat，在entity上建立索引
        search_word.dat，在word上建立索引
        """
        
    def solr_build(self):
        """
        读取search_entity.dat，建立entity索引；
        读取search_word.dat，建立word索引（两个索引可以共用，用不同的属性名应该不影响效率）
        注：手动bin/post ... 建立一个名为techproducts的solr索引，之后py向其中添加内容
        """
        solr = pysolr.Solr('http://192.9.200.93:8983/solr/techproducts')
        # 访问：http://192.9.200.93:8983/solr/#/~cores/techproducts
        # 清空数据
#        solr.delete(q='*:*')
        # 添加数据
        """
        solr.add([
                  {
                   "id": "doc_5",
                   "title": "A test document",
                   "content": "songjs_5",
                   },
                   {
                    "id": "doc_6",
                    "title": "The Banana: Tasty or Dangerous?",
                    "content": "songjs_6",
                    },
                    ])
        # 优化索引，以加快查询速度
        solr.optimize()
        """
        
        # 进行查询
        # 只对名称进行查询，找到之后返回某一属性列
        results = solr.search('title:"The Banana: Tasty or Dangerous?"')
#        results = solr.more_like_this(q='id:doc_2', mltfl='text')
        
#        results = solr.more_like_this(q='id:doc_2', mltfl='text')
        # 存储结果保存在results中 
        print("Saw {0} result(s).".format(len(results)))
        # 循环获取结果
        for result in results:
#            print("The title is '{0}'.".format(result['cat']))
            print("The title is '{0}'.".format(result['title']))
            

    def search(self, content):
        """
        对输入的一短文本，进行不同大小的切词
        由CGI向solr发出查询请求
        最后处理请求，找到当前查询文本段中的所有entity link
        """
        content = content_deal(content)
        content = content.split(' ')
        for i in len(content):
            # 每次访问当前词、当前词+后一词、前后各+一词
            # 这样不重不漏地访问完所有的1-gram/2-gram/3-gram词
            for word2 in content:
                word = word2
        
        solr = pysolr.Solr('http://192.9.200.93:8983/solr/techproducts')
        results = solr.search('title:"The Banana: Tasty or Dangerous?"')
        

if __name__ == '__main__':
    
    entity = Entity()
# entity.static();
#    print("songjs")
#    entity.solr_build()
#    entity.search("songjs_5 Jordan, Mackle DeprecationWarning: This module was deprecated in version 0.18 in favor of the model_selection module into which all the refactored classes and functions are moved. Also note tha")
    
    
