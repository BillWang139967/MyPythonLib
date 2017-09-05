## 修改配置文件工具


<!-- vim-markdown-toc GFM -->
* [功能](#功能)
* [使用](#使用)
    * [获取配置](#获取配置)
    * [更改配置](#更改配置)
* [二次开发](#二次开发)

<!-- vim-markdown-toc -->

## 功能

* 查找配置文件中配置和修改配置文件工具
* 更改配置只对特定项进行修改，如果没有则进行追加
* 更改配置项后的形式为 key=value 形式，如果要进行修改请看二次开发

## 使用

直接 `python file_util.py` 会输出使用提示

### 获取配置

使用方法：python file_util.py cfg_get 参数

如：
```
python file_util.py cfg_get ./config s3_addr
```
参数列表

> * config_file: 配置文件位置
> * item: 获取项
> * detail: 详细显示，显示 item 在多少行以及是否为注释状态等等

### 更改配置

功能：对某配置进行修改

使用方法：python file_util.py cfg_set 参数

如：
```
python file_util.py cfg_set ./config s3_addr 192.168.1.3
```
参数列表

> * config_file: 配置文件位置
> * item: 获取项
> * value: 某项要更改的值
> * commented: 配置的时候是否配置为注释状态

## 二次开发

更改配置项后的形式为 key=value 形式，如果要进行修改，比如修改为 `key="value"` 时可以修改程序

程序中`###############` 注释下的部分即为需要修改的地方
