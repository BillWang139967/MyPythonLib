---
layout: post
title:
subtitle:
date: 2016-11-21 20:10:35
category:
author: meetbill
tags:
   -
---

* [exception](#exception)
	* [str(e)](#stre)
	* [repr(e)](#repre)
	* [e.message](#emessage)
	* [采用traceback模块](#采用traceback模块)

# exception 

## str(e)

返回字符串类型，只给出异常信息，不包括异常信息的类型，如1/0的异常信息

'integer division or modulo by zero'

## repr(e)

给出较全的异常信息，包括异常信息的类型，如1/0的异常信息

"ZeroDivisionError('integer division or modulo by zero',)"

## e.message

获得的信息同str(e)

## 采用traceback模块

需要导入traceback模块，此时获取的信息最全，与python命令行运行程序出现错误信息一致。使用traceback.print_exc()打印异常信息到标准错误，就像没有获取一样，或者使用traceback.format_exc()将同样的输出获取为字符串。你可以向这些函数传递各种各样的参数来限制输出，或者重新打印到像文件类型的对象。
