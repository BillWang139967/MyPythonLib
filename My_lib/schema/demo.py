#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2018-12-16 17:29:44

# File Name: demo.py
# Description:

"""
import  schema

# 检查数字
print '----------------------int'
print schema.Schema(int).validate(123)
print schema.Schema(int).is_valid(123)

# 检查字符串
print '----------------------str'
# Regex 没有 is_valid 方法
print schema.Regex(r'^foo').validate('foobar')
print schema.Schema(lambda n: "foo" in n).is_valid('foobar')
print 'False:%s ' %  schema.Schema(lambda n: "foo" in n).is_valid('fobar')

# 检查字典
print '----------------------dict'
rules = {
    'name': schema.And(str, len),
    'age':  schema.And(schema.Use(int), lambda n: 18 <= n <= 99),
    schema.Optional('gender'): schema.And(str, schema.Use(str.lower),lambda s: s in ('squid', 'kid'))}

data = {'name': 'Sue', 'age': '28', 'gender': 'Squid'}

print schema.Schema(rules).validate(data)
print schema.Schema(rules).is_valid(data)

print '----------------------list-dict'
rules = [{
    'name': schema.And(str, len),
    'age':  schema.And(schema.Use(int), lambda n: 18 <= n <= 99),
    schema.Optional('gender'): schema.And(str, schema.Use(str.lower),lambda s: s in ('squid', 'kid'))}]

data = [{'name': 'Sue', 'age': '28', 'gender': 'Squid'},
        {'name': 'Sam', 'age': '42'},
        {'name': 'Sacha', 'age': '20', 'gender': 'KID'}]

print schema.Schema(rules).validate(data)
print schema.Schema(rules).is_valid(data)
