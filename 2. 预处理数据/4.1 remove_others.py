#! /usr/bin/python
import re
import time
import jieba
import string

# 去除非字母与数字与_的符号
with open("./data.seg") as f:
    content = f.readlines()
    for line in content:
#        if len(line)==0:
#print("error~~~~")
        for word in line:
            if word in "\n abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.":
                print(word,end="")
     
#print("finish~~~~~~~~~~~")
