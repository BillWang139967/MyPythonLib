## easyrun

一个 subprocess 模块的封装，可以更方便的进行系统调用

<!-- vim-markdown-toc GFM -->

* [1 安装](#1-安装)
* [2 使用方法](#2-使用方法)
    * [2.1 run](#21-run)
    * [2.2 run_capture](#22-run_capture)
        * [communicate() 和 wait() 使用上的区别](#communicate-和-wait-使用上的区别)
    * [2.3 run_capture_limited](#23-run_capture_limited)
    * [2.4 run_timeout](#24-run_timeout)
* [3 返回结果进行处理](#3-返回结果进行处理)
    * [3.1 返回结果处理为数组](#31-返回结果处理为数组)
    * [3.2 返回数据去掉换行符](#32-返回数据去掉换行符)
* [4 更新说明](#4-更新说明)

<!-- vim-markdown-toc -->

## 1 安装

```
将此目录下文件 easyrun.py 放到自己的程序目录中即可
```

## 2 使用方法

### 2.1 run

只单纯的执行，然后返回 linux run code 和执行状态

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
#### communicate() 和 wait() 使用上的区别

subprocess 就是开启一个子进程，自己去执行命令，这个子进程的状态肯定得收集，这时候就需要调用 wait 或者 communicate 了，手册上面也注明了这两个方法的特点：在数据超过 PIPE 的缓存时，wait 会阻塞进程；communicate 会把所有的数据都读取到内存中。
wait:
```
Warning
This will deadlock if the child process generates enough output to a stdout or stderr pipe such that it blocks waiting for the OS pipe buffer to accept more data. Use communicate() to avoid that.
```
communicate:
```
Note
The data read is buffered in memory, so do not use this method if the data size is large or unlimited
```
如果想要一行一行的读取的话，可以通过以下方法解决:

数据一行一行读取，读取完之后 wait，这样既保证了不会阻塞（PIPE 中数据有进有出，最后空了才 wait），又保证了不会占用大量主机内存（在内存中的数据只有一行 line）。
```
p1=subprocess.Popen(comm1,shell=True,stdout=subprocess.PIPE)
for line in p1.stdout:
    pass
p1.wait()
```

### 2.3 run_capture_limited

把输出的结果精简过，maxlines 是控制行数
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

## 3 返回结果进行处理

r.output 为字符串，日常使用时需要处理为对应类型的数据

### 3.1 返回结果处理为数组
使用此程序获取多行内容时处理方法，通过 split 方法将输出内容变为数组

```
r_list = r.output.split('\n')
while "" in r_list:
    r_list.remove("")
```
### 3.2 返回数据去掉换行符

比如 run_capture 获取的数据为一行字符串或者某个数字，则需要将其进行转换
```
r.output.replace("\n","")
```

## 4 更新说明


本程序在[原程序 easyrun](https://github.com/rfyiamcool/easyrun) 的基础上，修正了部分问题

> * v1.0.3 去掉 run_stream 和 run_async 函数
> * v1.0.2 修正 run_timeout 无法生效问题

