# MyPythonLib
<!-- vim-markdown-toc GFM -->

* [1 My_lib](#1-my_lib)
    * [1.1 终端界面 / 菜单相关](#11-终端界面--菜单相关)
    * [1.2 进程相关](#12-进程相关)
    * [1.3 Python 调用 shell](#13-python-调用-shell)
    * [1.4 配置文件及日志相关](#14-配置文件及日志相关)
    * [1.5 其他](#15-其他)
    * [1.6 XML 处理](#16-xml-处理)
* [2 Example](#2-example)
* [3 相关项目](#3-相关项目)
* [4 参加步骤](#4-参加步骤)

<!-- vim-markdown-toc -->

## 1 My_lib

### 1.1 终端界面 / 菜单相关

* [progressbar](My_lib/progressbar)--------------------Python 程序进度条
* [ttable](My_lib/ttable)------------------------------Linux 终端表格
* [command](My_lib/command_utils/)--------------------- 命令行执行加函数参数时，可以直接对函数操作
* [color](My_lib/color/)------------------------------- 终端 print 颜色

### 1.2 进程相关

* [daemon](My_lib/daemon)------------------------------ 守护进程模板
* [monitor_process](My_lib/monitor_process)------------ 检测某进程是否存在
* [mpms](My_lib/mpms/)---------------------------------Python 多进程 - 多线程任务队列
* [w_mpms](My_lib/w_mpms/)-----------------------------Python 多进程 - 多线程任务队列【简化版】

### 1.3 Python 调用 shell

* [easyrun](My_lib/easyrun/README.md)------------------Python 调用 shell 库

### 1.4 配置文件及日志相关

* [serverinfo_config](My_lib/serverinfo_config)-------- 查看 Linux 信息和修改 Linux 配置文件
* [log](My_lib/log_utils/)----------------------------- 根据日志大小轮转日志
* [file_utils](My_lib/file_utils/)--------------------- 对配置文件进行获取配置以及修改配置
* [validator](My_lib/validator)------------------------ 函数参数检查

### 1.5 其他

* [mysqlORM](My_lib/mysqlORM/)-------------------------MySQLORM
* [query_ip](My_lib/query_ip/)------------------------- 根据 IP 获取地址位置信息

### 1.6 XML 处理

* [xmltodict](./My_lib/xmltodict/)--------------------- 将 xml 转为字典或者字典转为 xml

## 2 Example

* [相关 wiki](https://github.com/meetbill/MyPythonLib/wiki)
* [Python 基础学习](./Example/python_base/README.md)
* [Python 交互模式自动补全](./Example/python_interactive/README.md)

## 3 相关项目

* [运维实践指南相关程序](https://github.com/meetbill/op_practice_code)
* [Linux 运维工具](https://github.com/meetbill/linux_tools)

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
