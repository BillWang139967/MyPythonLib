## blog


<!-- vim-markdown-toc GFM -->

* [1 使用方法](#1-使用方法)
    * [1.1 全局日志配置](#11-全局日志配置)
    * [1.2 针对不同的用途或模块，指定不同的日志](#12-针对不同的用途或模块指定不同的日志)

<!-- vim-markdown-toc -->

日志库

Function

>* 可设置是否输出到终端，如果输出到终端，则彩色显示
>* 可设置日志路径及输出日志级别
>* 可设置日志轮转大小及保存个数

## 1 使用方法

### 1.1 全局日志配置

```
import blog
blog.init_log("./log/common.log")
```
> * 配置全局日志配置后，默认 info 级别以上的日志会打印到 "./log/common.log.log"
> * warning 级别以上的日志会打印到 "./log/common.log.log.wf" 中

### 1.2 针对不同的用途或模块，指定不同的日志

```
import blog
debug = True
logpath = "./log/test.log"
logger = blog.Log(
    logpath,
    level="debug",
    logid="meetbill",
    is_console=debug,
    mbs=5,
    count=5)

logstr = "helloworld"
logger.error(logstr)
logger.info(logstr)
logger.warn(logstr)
logger.debug(logstr)
```
每个 logger 都有个名字，以 ‘.’ 来划分继承关系。名字为空的就是 root_logger, 默认所有的日志都会出现在全局的  logging 配置的日志文件中

如何让自定义 logger 的内容不出现在全局的 logging 里面，其中起作用的就是如下一行
```
self._logger.propagate=False
```
