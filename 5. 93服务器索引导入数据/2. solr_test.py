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
from urllib2 import *
import ast
import pysolr
import string

class Entity():
    
    
    def __init__(self):
        return ;
            
        
    def solr_test(self):
        """
        读取entity.final，建立entity索引；
        读取word.final，建立word索引  
        """
        solr = pysolr.Solr('http://192.9.200.93:8983/solr/techproducts')

        # 进行查询
        # 只对名称进行查询，找到之后返回某一属性列
        results = solr.search('id:"August_9"') # Azerbaijan
        # 存储结果保存在results中 
        print("Saw {0} result(s).".format(len(results)))
        # 循环获取结果
        for result in results:
#            print("The title is '{0}'.".format(result['cat']))
            print("The url is '{0}'.".format(result['title']))
            

            

if __name__ == '__main__':
    
    entity = Entity()
#    print("songjs")
    entity.solr_test()
#    entity.search("songjs_5 Jordan, Mackle DeprecationWarning: This module was deprecated in version 0.18 in favor of the model_selection module into which all the refactored classes and functions are moved. Also note tha")
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    


