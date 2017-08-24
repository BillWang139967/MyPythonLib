## xmltodict
<!-- vim-markdown-toc GFM -->
* [xml 转 dict](#xml-转-dict)
    * [方法](#方法)
    * [字典和 json 的区别](#字典和-json-的区别)
* [dict 转 xml](#dict-转-xml)

<!-- vim-markdown-toc -->

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
