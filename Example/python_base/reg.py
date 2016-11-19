#!/usr/bin/python
#coding=utf8
import re
#---------------------正则-匹配---------------------
print(re.match(r'^\d{3}-\d{3,8}$', '010-85112365'))
print(re.match(r'^\d{3}\-\d{3,8}$', '010-85112365'))

#---------------------正则-分割---------------------
print (''''a b   c'.split(' '):''','a b   c'.split(' '))
print ('''re.split(r'\s+', 'a b  c'):''', re.split(r'\s+', 'a b  c'))
print (re.split(r'[\s\,]+', 'a,b, c  d'))
print (re.split(r'[\s|\,]+', 'a,b, c  d'))
print (re.split(r'[\s\,\;]+', 'a,b;; c  d'))

#---------------------正则-分组---------------------
m = re.match(r'^(\d{3})-(\d{3,8})$', '010-123456')
print (m)
print (m.group(0))
print (m.group(1))
print (m.group(2))

#---------------------正则-贪婪匹配---------------------
print (re.match(r'^(\d+)(0*)$', '102300').groups())
print (re.match(r'^(\d+?)(0*)$', '102300').groups())
