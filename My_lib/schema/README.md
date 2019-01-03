## schema
<!-- vim-markdown-toc GFM -->

* [1 功能](#1-功能)
* [2 使用方法](#2-使用方法)
    * [2.1 检查数字](#21-检查数字)
    * [2.2 检查字符串](#22-检查字符串)
    * [2.3 检查字典](#23-检查字典)
    * [2.4 检查列表中字典](#24-检查列表中字典)
* [3 管理此目录](#3-管理此目录)
* [4 FAQs](#4-faqs)
    * [4.1 Schema 传入字典很好用，但是我有的数据是可选的，也就是说有的 key 可以不提供怎么办？](#41-schema-传入字典很好用但是我有的数据是可选的也就是说有的-key-可以不提供怎么办)
    * [4.2 我想让 Schema 只验证传入字典中的一部分数据，可以有多余的 key 但是不要抱错，怎么做？](#42-我想让-schema-只验证传入字典中的一部分数据可以有多余的-key-但是不要抱错怎么做)
    * [4.3 Schema 抛出的异常信息不是很友好，我想自定义错误信息，怎么办？](#43-schema-抛出的异常信息不是很友好我想自定义错误信息怎么办)

<!-- vim-markdown-toc -->

## 1 功能

参数校验

> * [原项目地址](https://github.com/keleshev/schema)

## 2 使用方法

### 2.1 检查数字
```
import  schema

# 检查数字
print '----------------------int'
print schema.Schema(int).validate(123)
print schema.Schema(int).is_valid(123)
```
### 2.2 检查字符串
```
# 检查字符串
print '----------------------str'
# Regex 没有 is_valid 方法
print schema.Regex(r'^foo').validate('foobar')
print schema.Schema(lambda n: "foo" in n).is_valid('foobar')
print 'False:%s ' %  schema.Schema(lambda n: "foo" in n).is_valid('fobar')

```
### 2.3 检查字典
```

# 检查字典
print '----------------------dict'
rules = {
    'name': schema.And(str, len),
    'age':  schema.And(schema.Use(int), lambda n: 18 <= n <= 99),
    schema.Optional('gender'): schema.And(str, schema.Use(str.lower),lambda s: s in ('squid', 'kid'))}

data = {'name': 'Sue', 'age': '28', 'gender': 'Squid'}

print schema.Schema(rules).validate(data)
print schema.Schema(rules).is_valid(data)

```
### 2.4 检查列表中字典
```
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
```
## 3 管理此目录

> * https://github.com/keleshev/schema
>   * 将原项目中的 schema.py 重命名为 `schema/__init__.py`

## 4 FAQs

### 4.1 Schema 传入字典很好用，但是我有的数据是可选的，也就是说有的 key 可以不提供怎么办？
```
from schema import Optional, Schema


Schema({'name': str, Optional('age'): int}).validate({'name': 'foobar'})
{'name': 'foobar'}
Schema({'name': str, Optional('age', default=18): int}).validate({'name': 'foobar'})
{'age': 18, 'name': 'foobar'}
```
### 4.2 我想让 Schema 只验证传入字典中的一部分数据，可以有多余的 key 但是不要抱错，怎么做？
```
Schema({'name': str, 'age': int}, ignore_extra_keys=True).validate({'name': 'foobar', 'age': 100, 'sex': 'male'})
{'age': 100, 'name': 'foobar'}
```
### 4.3 Schema 抛出的异常信息不是很友好，我想自定义错误信息，怎么办？
Schema 自带的类（Use、And、Or、Regex、Schema 等）都有一个参数 error，可以自定义错误信息
```
Schema({'name': str, 'age': Use(int, error='年龄必须是整数')}).validate({'name': 'foobar', 'age': 'abc'})
SchemaError: 年龄必须是整数
```
