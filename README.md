# MyPythonLib
<!-- vim-markdown-toc GFM -->
* [My_lib](#my_lib)
    * [终端界面/菜单相关](#终端界面菜单相关)
    * [进程相关](#进程相关)
    * [配置文件及日志相关](#配置文件及日志相关)
    * [其他](#其他)
    * [XML 处理](#xml-处理)
* [Example](#example)
* [相关项目](#相关项目)
* [参加步骤](#参加步骤)

<!-- vim-markdown-toc -->

## My_lib

### 终端界面/菜单相关 

* [progressbar](My_lib/progressbar)--------------------python 程序进度条
* [ttable](My_lib/ttable)------------------------------Linux 终端表格
* [command](My_lib/command_utils/)---------------------命令行执行加函数参数时，可以直接对函数操作

### 进程相关

* [daemon](My_lib/daemon)------------------------------守护进程模板
* [monitor_process](My_lib/monitor_process)------------检测某进程是否存在

### 配置文件及日志相关

* [serverinfo_config](My_lib/serverinfo_config)--------查看linux信息和修改linux配置文件
* [log](My_lib/log_utils/)-----------------------------根据日志大小轮转日志
* [file_utils](My_lib/file_utils/)---------------------对配置文件进行获取配置以及修改配置

### 其他

* [mysqlORM](My_lib/mysqlORM/)-------------------------mysqlORM
* [query_ip](My_lib/query_ip/)-------------------------根据 IP 获取地址位置信息

### XML 处理

* [xmltodict](./My_lib/xmltodict/)---------------------将 xml 转为字典或者字典转为 xml

## Example

* [相关wiki](https://github.com/BillWang139967/MyPythonLib/wiki)
* [python 基础学习](./Example/python_base/README.md)

## 相关项目

* [运维实践指南相关程序](https://github.com/BillWang139967/op_practice_code)
* [Linux 运维工具](https://github.com/BillWang139967/linux_tools)

## 参加步骤

* 在 GitHub 上 `fork` 到自己的仓库，然后 `clone` 到本地，并设置用户信息。
```
$ git clone https://github.com/BillWang139967/MyPythonLib.git
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
$ git remote add upstream https://github.com/BillWang139967/MyPythonLib.git
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
$ git push -f origin master
```
