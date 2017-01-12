#! /usr/bin/python
import re
import time
import jieba
import string

# 读入停用词
with open("./data.seg2") as f:
    content = f.readlines()
    for line in content:
        if len(line)==0:
            print("error~~~~")
     
print("finish~~~~~~~~~~~")
