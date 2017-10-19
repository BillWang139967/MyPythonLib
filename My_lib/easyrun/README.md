## easyrun

一个subprocess模块的封装,可以更方便的进行系统调用

<!-- vim-markdown-toc GFM -->
* [1 安装](#1-安装)
* [2 使用方法](#2-使用方法)
    * [2.1 run](#21-run)
    * [2.2 run_capture](#22-run_capture)
    * [2.3 run_capture_limited](#23-run_capture_limited)
    * [2.4 run_timeout](#24-run_timeout)
* [3 更新说明](#3-更新说明)

<!-- vim-markdown-toc -->

## 1 安装

```
将此目录下文件 easyrun.py 放到自己的程序目录中即可
```

## 2 使用方法

### 2.1 run

只单纯的执行，然后返回linux run code和执行状态

```
>>> import easyrun
>>> r = easyrun.run('uptime')
 04:06:37 up 2 min,  1 user,  load average: 0.20, 0.19, 0.08
>>> r.output
>>> r.success
True
>>> r.retcode
0
```
### 2.2 run_capture
捕捉所有的执行结果
```
>>> r = easyrun.run_capture('uptime')
>>> r.output
' 04:07:16 up 2 min,  1 user,  load average: 0.11, 0.17, 0.08\n'
>>> r.success
True
>>> r.retcode
0
```
例子
```
from easyrun import run_capture

r = run_capture('ls -la')
if r.success:
    print(r.output)
else:
    print("Error: '%s' exit code %s" % (r.command, r.retcode))
    print("         ...")
    # print last three lines of output
    for line in r.output.splitlines()[-3:]:
        print("       %s" % line)
```

### 2.3 run_capture_limited

把输出的结果精简过,maxlines是控制行数
```
print(run_capture_limited('ls', maxlines=2).output)
```

### 2.4 run_timeout

设置程序运行时长

如下是获取 ES 状态示例，访问的服务器无响应时，一直无法返回结果，通过设置 timeout 以免程序阻塞

```
    >>>import easyrun
    >>>r = easyrun.run_timeout('curl -sXGET http://IP:9200/_cluster/health/?pretty', timeout=3)
    >>>r.success
    False
    >>>r.retcode
    124
    >>>r.output
    'timeout'
```

## 3 更新说明


本程序在[原程序 easyrun](https://github.com/rfyiamcool/easyrun)的基础上，修正了部分问题

> * v1.0.2 修正 run_timeout 无法生效问题

