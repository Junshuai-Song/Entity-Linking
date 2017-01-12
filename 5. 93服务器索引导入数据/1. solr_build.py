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
    
    
    def __init__(self):
        return ;
            
        
    def solr_build(self):
        """
        读取entity.final，建立entity索引；
        读取word.final，建立word索引  
        """
        solr = pysolr.Solr('http://192.9.200.93:8983/solr/techproducts')
        # 访问：http://192.9.200.93:8983/solr/#/~cores/techproducts
        # 清空数据
        solr.delete(q='*:*')
        # 添加数据
        print("清空索引数据，下面开始导入数据...")
        
        with open('./word.final') as f:
            self.words = f.readlines()
        with open('./entity.final') as f:
            self.entities = f.readlines()
        for i in range(len(self.entities)):
            line = self.entities[i]
            lines = line.split(' ')
            entity = lines[0]
            link = lines[1]
            topic_entity = " ".join(lines[2:])
            solr.add([
                  {
                   "id": entity,
                   "title": link,
                   "content": topic_entity,
                   },
                    ])
            if i%10==0:
                print(i)
            
        for i in range(len(self.words)):
            line = self.words[i]
            lines = line.split(' ')
            word = "ssssss" + lines[0];
            topic_word = " ".join(lines[1:])
            """
            print(entity)
            print(link)
            print(topic_entity)
            print(word)
            print(topic_word)
            return ;
            """
            
            solr.add([
                  {
                   "id": word,
                   "title": "***",
                   "content": topic_word,
                   },
                    ])
            if i%10==0:
                print(i)
        # 优化索引，以加快查询速度
        solr.optimize()
        
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
        results = solr.search('id:"August_9"') # Azerbaijan
#        results = solr.more_like_this(q='id:doc_2', mltfl='text')
        
#        results = solr.more_like_this(q='id:doc_2', mltfl='text')
        # 存储结果保存在results中 
        print("Saw {0} result(s).".format(len(results)))
        # 循环获取结果
        for result in results:
#            print("The title is '{0}'.".format(result['cat']))
            print("The url is '{0}'.".format(result['title']))
            

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
#    print("songjs")
    entity.solr_build()
#    entity.search("songjs_5 Jordan, Mackle DeprecationWarning: This module was deprecated in version 0.18 in favor of the model_selection module into which all the refactored classes and functions are moved. Also note tha")
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    


