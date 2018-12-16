## schema
<!-- vim-markdown-toc GFM -->

* [1 功能](#1-功能)
* [2 使用方法](#2-使用方法)
    * [2.1 检查数字](#21-检查数字)
    * [2.2 检查字符串](#22-检查字符串)
    * [2.3 检查字典](#23-检查字典)
    * [2.4 检查列表中字典](#24-检查列表中字典)
* [3 管理此目录](#3-管理此目录)

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
