## 统计代码行数


<!-- vim-markdown-toc GFM -->

* [usage](#usage)
* [思路](#思路)
    * [统计 python 文件中的代码，注释，空白对应的行数](#统计-python-文件中的代码注释空白对应的行数)

<!-- vim-markdown-toc -->

## usage
```
python ./py_count.py count dir_name
```
## 思路
### 统计 python 文件中的代码，注释，空白对应的行数

其实代码和空白行很好统计，难点是注释行
```
python 中的注释分为以#开头的单行注释

或者以'''开头以'''结尾 或以"""开头以"""结尾的文档注释，如：

'''

hello world

'''和

'''

hello world'''
```

思路是用 is_comment 记录是否存在多行注释，如果不存在，则判断当前行是否以'''开头，是则将 is_comment 设为 True, 否则进行空行、当前行注释以及代码行的判断，

如果 is_comment 已经为 True 即，多行注释已经开始，则判断当前行是否以'''结尾，是则将 is_comment 设为 False, 同时增加注释的行数。表示多行注释已经结束，反之继续，此时多行注释还未结束
