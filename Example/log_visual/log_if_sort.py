#!/usr/bin/python
#coding=utf8
"""
# Author: Bill
# Created Time : 2016-06-02 23:26:54

# File Name: log_if_sort.py
# Description:针对某个请求根据访问次数将每个IP排序

"""
import re
f = open('./acc.log')
res = {}
sum=0
for l in f:
    try:
        arr = re.split(' |\t',l)
        # 获取ip url 和status
        module = arr[3]
        ip = arr[4]
        status = arr[7]
        interface = arr[8]
        
        #return_info = arr[9]
        if interface != 'getUserQuota':
            continue
        # ip url 和status当key，每次统计+1
        res[(ip)] = res.get((ip),0)+1
    except:
        print l
# 生成一个临时的list
res_list = [(k,v) for k,v in res.items()]
# 按照统计数量排序
for k in sorted(res_list,key=lambda x:x[1],reverse=True):
    sum=sum+1
    print k
    
print sum
