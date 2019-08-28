---
layout: post
title:
subtitle:
date: 2019-08-27 23:45:46
category:
author: meetbill
tags:
   -
---
## redis-rdb-tools

<!-- vim-markdown-toc GFM -->

* [1 安装](#1-安装)
* [2 导出 RDB 数据到 csv 文件](#2-导出-rdb-数据到-csv-文件)
* [3 把 RDB 文件导出到 JSON](#3-把-rdb-文件导出到-json)
* [4 比较功能](#4-比较功能)
* [5 协议转换功能](#5-协议转换功能)

<!-- vim-markdown-toc -->
## 1 安装

> 地址
```
https://github.com/sripathikrishnan/redis-rdb-tools
```
> 使用
```
cd redis-rdb-tools
cp rdbtools/cli/rdb.py .
chmod +x rdb.py
```
## 2 导出 RDB 数据到 csv 文件
```
cd redis-rdb-tools
./rdb.py -c memory dump.rdb > result.csv
```
csv(Excel) 文件中的列信息如下：

> * database：数据库编号
> * type：数据结构类型
> * key：k-v 中的 key
> * memory_size(bytes)：内存占用（字节数）
> * encoding：编码
> * num_elements：集合元素数
> * len_largest_element：集合中最长的一个元素的长度
> * expiry：过期时间

> 输出大于 1M 的 key
```
python rdb.py  -c memory ./dump.rdb --bytes 1024000
```

## 3 把 RDB 文件导出到 JSON
```
cd redis-rdb-tools
./rdb.py -c json dump.rdb > result.json
```
为了更简洁，文档后边将只使用安装的方式进行举例
注意，这里是把 RDB 文件中的数据导出，而不是把统计数据导出。
json 结果举例：

[
  {
    "s1": [
      "f",
      "b",
      "a",
      "e",
      "d",
      "c"
    ],
    "key2": "value22222",
    "list1": [
      "k1",
      "k2",
      "k333333",
      "k4"
    ],
    "key3": "value3",
    "key1": "value1",
    "z1": {
      "a": 1,
      "b": 2,
      "c": 3
    }
  }
]
还可以通过例如如下方式进行更细粒度的筛选数据

> 根据表达式过滤 key 的范围
```
rdb -c json --key "user.*" dump.rdb
```
> 只导出数据库 2 中的 hash 数据
```
rdb -c json --db 2 --type hash --key "a.*" dump.rdb
```
## 4 比较功能
这个工具提供了简单的针对 diff 做优化的格式化输出功能。
例如比较 dump1.rdb 和 dump2.rdb，如下操作：

```
# 分别使用 diff 后输出到文件
rdb -c diff dump1.rdb | sort > dump1.txt
rdb -c diff dump2.rdb | sort > dump2.txt
# 使用任意一个 diff 工具进行比较
kdiff3 dump1.txt dump2.txt
如果文件太大，可以加上—key=regex 等参数进行数据筛选。
```

## 5 协议转换功能
把 RDV 文件转换成 redis protocol

```
rdb -c protocol dump.rdb
*4
$4
HSET
$9
users:123
$9
firstname
$8
Sripathi
```
同样，如果只想指定部分数据，可以使用—key 等命令进行过滤。这也为数据分片提供了可能。使用—key 将数据分成多片，通过 redis protocol 格式进行网络传输。

导出图形化统计网页功能
这个功能是原作者留下的彩蛋，相当实用，能够把 RDB 文件中的数据进行统计后，以饼图和柱状图的方式，输出到网页上。
由于当时原作者还未将该功能放到安装包里整合成命令，所以需要进到源码目录中去执行这个工具。
```
cd redis-rdb-tools/rdbtools/cli/
python redis_profiler.py /yourpath/dump.rdb > show.html
```
需要注意的是，html 中依赖 google 的 cdn 中的一些工具，暂时需要翻墙才能渲染出来……

在代码中使用 Parser
通过继承 RdbCallback 类，可以自己通过回调实现更多功能。

```
import sys
from rdbtools import RdbParser, RdbCallback
class MyCallback(RdbCallback) :
    ''' Simple example to show how callback works.
        See RdbCallback for all available callback methods.
        See JsonCallback for a concrete example
    '''
    def set(self, key, value, expiry):
        print('%s = %s' % (str(key), str(value)))
    def hset(self, key, field, value):
        print('%s.%s = %s' % (str(key), str(field), str(value)))
    def sadd(self, key, member):
        print('%s has {%s}' % (str(key), str(member)))
    def rpush(self, key, value) :
        print('%s has [%s]' % (str(key), str(value)))
    def zadd(self, key, score, member):
        print('%s has {%s : %s}' % (str(key), str(member), str(score)))
callback = MyCallback()
parser = RdbParser(callback)
parser.parse('dump.rdb')
```
