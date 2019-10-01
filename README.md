# MyPythonLib
<!-- vim-markdown-toc GFM -->

* [1 My_lib](#1-my_lib)
    * [1.1 终端界面 / 菜单相关](#11-终端界面--菜单相关)
    * [1.2 进程相关](#12-进程相关)
    * [1.3 配置文件及日志相关](#13-配置文件及日志相关)
    * [1.4 其他](#14-其他)
    * [1.5 Debug](#15-debug)
    * [1.6 DB/Redis](#16-dbredis)
* [2 Example](#2-example)
    * [2.1 教程](#21-教程)
    * [2.2 相关笔记](#22-相关笔记)
* [3 相关项目](#3-相关项目)
* [4 参加步骤](#4-参加步骤)

<!-- vim-markdown-toc -->

## 1 My_lib

### 1.1 终端界面 / 菜单相关

* Python 程序进度条 ---------------------------[progressbar](My_lib/progressbar)
* Linux 终端表格 ------------------------------[ttable](My_lib/ttable)
* 命令行执行加函数参数时，可以直接对函数操作 --[command](My_lib/command_utils/)
* 终端 print 颜色 -----------------------------[color](My_lib/color/)

### 1.2 进程相关

* 守护进程模板 --------------------------------[daemon](My_lib/daemon)
* 检测某进程是否存在 --------------------------[monitor_process](My_lib/monitor_process)
* Python 多进程 - 多线程任务队列 --------------[mpmt](https://github.com/meetbill/mpmt)
* Python 调用 shell 库 ------------------------[easyrun](My_lib/easyrun/README.md)

### 1.3 配置文件及日志相关

* 查看 Linux 信息和修改 Linux 配置文件 --------[serverinfo_config](My_lib/serverinfo_config)
* 根据日志大小轮转日志 ------------------------[log](My_lib/log_utils/)
* 对配置文件进行获取配置以及修改配置 ----------[file_utils](My_lib/file_utils/)
* 参数检查
  * 函数参数检查 ------------------------------[schema](My_lib/schema)
* 将 xml 转为字典或者字典转为 xml -------------[xmltodict](./My_lib/xmltodict/)

### 1.4 其他

* 根据 IP 获取地址位置信息 --------------------[query_ip](My_lib/query_ip/)

### 1.5 Debug

* 极简 DeBug 工具 PySnooper -------------------[PySnooper](https://github.com/cool-RR/PySnooper)

### 1.6 DB/Redis

* 轻量化 MySQL orm ----------------------------[Peewee](My_lib/peewee)
* Python 连接 MySQL 的库 PyMySQL --------------[PyMySQL](My_lib/pymysql)
* 分析 Redis RDB 工具 -------------------------[redis-rdb-tools](My_lib/redis-rdb-tools)

## 2 Example

### 2.1 教程

* [微软 Python 教程](https://github.com/microsoft/c9-python-getting-started)

### 2.2 相关笔记

* [相关 wiki](https://github.com/meetbill/MyPythonLib/wiki)
* [Python 基础学习](./Example/python_base/README.md)
* [Python 交互模式自动补全](./Example/python_interactive/README.md)
* [Python 统计文件夹中代码行数](./Example/python_count)
* [Pytest](./My_lib/pytest)

## 3 相关项目

> * [运维实践指南相关程序](https://github.com/meetbill/op_practice_code)
> * [Linux 运维工具](https://github.com/meetbill/linux_tools)
> * Python 常用库集合[星图](https://github.com/meetbill/x-lib)

## 4 参加步骤

* 在 GitHub 上 `fork` 到自己的仓库，然后 `clone` 到本地，并设置用户信息。
```
$ git clone https://github.com/meetbill/MyPythonLib.git
$ cd MyPythonLib
$ git config user.name "yourname"
$ git config user.email "your email"
```
* 修改代码后提交，并推送到自己的仓库。
```
$ #do some change on the content
$ git commit -am "Fix issue #1: change helo to hello"
$ git push
```
* 在 GitHub 网站上提交 pull request。
* 定期使用项目仓库内容更新自己仓库内容。
```
$ git remote add upstream https://github.com/meetbill/MyPythonLib.git
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
$ git push -f origin master
```
