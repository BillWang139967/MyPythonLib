## xmltodict
<!-- vim-markdown-toc GFM -->
* [使用](#使用)
    * [xml 转 dict](#xml-转-dict)
        * [方法](#方法)
        * [字典和 json 的区别](#字典和-json-的区别)
    * [dict 转 xml](#dict-转-xml)
        * [范例](#范例)
* [FAQ 及需注意内容](#faq-及需注意内容)
    * [xml 转 dict 时报错](#xml-转-dict-时报错)
    * [xml 转 dict 时注意](#xml-转-dict-时注意)

<!-- vim-markdown-toc -->
# 使用

## xml 转 dict

### 方法

parse

**注**：输入值为 xml 字符串，需要去掉 xml 声明 (<?xml version="1.0" encoding="UTF-8"?>), 如果网页获取的 xml 含有声明可以用下面方法去掉声明

```
new_xml = old_xml.split('?>')[1]
```

### 字典和 json 的区别

在 python 中，字典的输出内容跟 json 格式内容一样，但是字典的格式是字典，json 的格式是字符串，所以在传输的时候（特别是网页）要转换使用

* 编码：把一个 Python 对象编码转换成 Json 字符串 ---json.dumps()
* 解码：把 Json 格式字符串解码转换成 Python 对象 ---json.loads()

## dict 转 xml

unparse

### 范例

```
import xmltodict


try:  # pragma no cover
    from collections import OrderedDict
except ImportError:  # pragma no cover
    try:
        from ordereddict import OrderedDict
    except ImportError:
        OrderedDict = dict

data = OrderedDict()
data["mydocument"] = OrderedDict()
data["mydocument"]["@has"] = "an attribute"
data["mydocument"]["and"] = OrderedDict()
data["mydocument"]["and"]["many"] = []
data["mydocument"]["and"]["many"].append("elements")
data["mydocument"]["and"]["many"].append("more elements")
data["mydocument"]["plus"] = OrderedDict()
data["mydocument"]["plus"]["@a"] = "complex"
data["mydocument"]["plus"]["#text"] = "elements as well"

print xmltodict.unparse(data,pretty=True)

```

# FAQ 及需注意内容

## xml 转 dict 时报错

报错如下

```
xml.parsers.expat.ExpatError: not well-formed (invalid token): line 11, column 47
```
上面提示是在 xml 的第 11 行的第 47 个字符那有问题，查看的时候查看下上行是否有错误

检查下是否双引号使用了中文，xml 格式错误等等

## xml 转 dict 时注意

我在本地的操作如下

```
A 机器通过 dict 生成 xml，发送给机器 B
B 机器接受到 xml 后转为 dict
```
其实这个时候，A 的 dict 和 B 转后的 dict 是可能不一样的

例如下面场景
```
"ROW":[
    {
        "STATUS": 2, 
        "MSG": "ERR"
    }
]

```
原字典中的 value 是个列表，但是列表中只有一项，转为 xml 然后转为 dick 时就会变为如下结果
```
"ROW":{
        "STATUS": 2, 
        "MSG": "ERR"
    }
```
