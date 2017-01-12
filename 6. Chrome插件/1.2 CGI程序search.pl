#! python
# -*- coding:utf-8 -*-
import pysolr
import cgi
import cgitb

print "Content-type: text/plain; charset=iso-8859-1\n";


form = cgi.FieldStorage()
content = form.getvalue('content')


# !/usr/bin/python


import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
#import matplotlib as mpl
#import matplotlib.pyplot as plt
import random
import math
import sys
import re
import ast
import pysolr
import jieba
import string

class Entity():
    
    
    def __init__(self):
        return ;
            
        
    def solr_search(self,content):
        """
        读取entity.final，建立entity索引；
        读取word.final，建立word索引  
        """
        # 预处理content，将一段话分割成句子的形式
        # 注：不要跨段选文字！会出现问题，因为不识别\n回车，所以上一行末尾会对下一行初始有一定影响（非要选就要认识到这点）
        with open("./stopwords.txt") as f:
            stopwords = set([i.strip() for i in f.readlines()])

        lst = []
        for word in jieba.cut(content):
            if word not in stopwords and word != ' ' and word!='  ':
                lst.append(word)
                #print(word)
                
        topic_word = [0.0]*50  #50个主题
        solr = pysolr.Solr('http://192.9.200.93:8983/solr/techproducts')
        # -- print("----topic_word,查询单词----")
        for word in lst:
            results = solr.search('id:' + 'ssssss' + word) 
            # -- print("Saw {0} result(s).".format(len(results)))
        # 循环获取结果
            for result in results:
                if str(result['title'][0])=="***":
                    # -- print("The topic is '{0}'.".format(result['content']))
                    topic = str(result['content']).split(' ')
                    topic[0] = topic[0][3:]
                    # print(topic_word)
                    topic[49] = topic[49][:-4]
    
                    # 下面为了避免频率高的词掩盖掉重要的词，这里改为增加概率分布（不再加词频）
                    count = 0.0
                    for t in range(len(topic)):
                        count += (float)(topic[t])
                    if(count==0):
                        count=1
                    for t in range(len(topic)):
                        topic_word[t] += ((float)(topic[t])/count)  # 这里加成

        
        # -- print("\n----1/2/3-gram词,查询entity----")
        # 1/2/3-gram词
        length = len(lst)
        for i in range(length-3):
            lst.append(lst[i]+"_"+lst[i+1])
            lst.append(lst[i]+"_"+lst[i+1]+"_"+lst[i+2])
        lst.append(lst[length-2]+"_"+lst[length-1])
        
        # 排序，分别进行查询
        lst.sort()
        query = set(lst)
        lst = list(query)
        lst.sort()
        
        ans = []
        # 下面进行查询
        for word in lst:
            info = []
            results = solr.search('id:' + word)
            # -- print("Saw {0} result(s).".format(len(results)))
            # 循环获取结果
            for result in results:
                w = (str)(result['title'][0])
                if w!="***":   # 确保这里找的不是word，是entity
                    # -- print("The url is '{0}'.".format(result['title']))
                    topic = ((str)(result['content'])).split(' ')
                    cnt = 0.0
                    # for t in range(len(topic)):
                    #     print(topic[t])
                    topic[0] = topic[0][3:] # topic[0]是u'0.0123 的形式； 另外把最后一个\n'也去掉
                    for t in range(len(topic)-1):
                        cnt += (float(topic_word[t]) * float(topic[t]))
                    info.append(word)
                    info.append(str(result['title'][0]))
                    info.append(cnt)
                    ans.append(info)
                    info = []

        # 把查询到的entity输出看一下
        # -- print("----查询到的entity结果(含相似度)----")
        # -- print(ans)

        # -- print("----筛选ing----")
        ret = []
        # 对ans中的结果按照相似度value从大到小进行删除，为了避免出现重复单词，每次删除需要去掉所有相关联的词
        while 1:
            if(len(ans)<=0):
                break
            wei = 0
            maxc = -1.0
            for i in range(len(ans)):
                if(ans[i][2] > maxc):
                    maxc = ans[i][2]
                    wei = i
            r = []
            r.append(ans[wei][0])
            r.append(ans[wei][1])
            ret.append(r)
            r = []

            ans2 = []
            # 删除包含当前词的所有项
            s = ans[wei][0].split('_')
            for i in range(len(ans)):
                flag=0
                for j in s:
                    if(j in ans[i][0]):
                        flag=1
                        break
                if(flag!=1):
                    ans2.append(ans[i])
            ans = ans2;
            ans2 = []
        
        # ret中保存的是所有的查询结果
        # -- print("----筛选后的结果----")
        answer = []
        for r in ret:
            answer.append(" ".join(r))
        print(";".join(answer))
        
        # 最后将查询结果返回chrome即可！




    
entity = Entity()
#    print("songjs")
entity.solr_search(content)
#    entity.search("songjs_5 Jordan, Mackle DeprecationWarning: This module was deprecated in version 0.18 in favor of the model_selection module into which all the refactored classes and functions are moved. Also note tha")
    
    
    



    
    
    
    
    
    
    
    

    




