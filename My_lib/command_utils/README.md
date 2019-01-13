## command_utils

<!-- vim-markdown-toc GFM -->

* [1 command_class](#1-command_class)
* [2 command](#2-command)
    * [2.1 使用](#21-使用)
    * [2.2 内部原理](#22-内部原理)
        * [2.2.1 根据 globals 内置函数获取全部全局变量](#221-根据-globals-内置函数获取全部全局变量)
        * [2.2.2 获取函数的参数](#222-获取函数的参数)

<!-- vim-markdown-toc -->

## 1 command_class

作用：方便命令行调用模块中类中的方法（推荐）, 更新程序时仅需添加方法，非常方便

```
[root@meetbill ~]# python command_class.py
usage: python command_class.py function param [options]

optional arguments:
  -h, --help  show this help message and exit
  None
  Python Library Documentation: class ceshi_class in module __main__
  class ceshi_class
   |  ceshi
   |
   |  Methods defined here:
   |
   |  output(self, str_info)
   |      eg:python command_class.py output "hello world"
   |
   |  output2(self, str_info='happy')
   |      eg:python command_class.py output2 "hello world"

```

直接输入 `python command_class.py output "hello world"`即可调用此模块 `ceshi_class` 类中的 output 方法

## 2 command

作用：方便调用模块中的方法

```
#python command.py
Usage:
command.py hello 'str_info'
```
### 2.1 使用

不太清楚参数的含义时，可以直接执行方法，而不带参数
```
#python command.py hello
Usage:
    python hello 'str_info'
        str_info: string
hello() takes exactly 1 argument (0 given)
Traceback (most recent call last):
  File "command.py", line 24, in <module>
    r = func(*args)
TypeError: hello() takes exactly 1 argument (0 given)
```

此时会输出方法使用说明（参数说明在函数名下填写）和对应错误信息

### 2.2 内部原理

#### 2.2.1 根据 globals 内置函数获取全部全局变量

globals() 函数会以字典类型返回当前位置的全部全局变量。
```
{
	'Ceshi_class': < class __main__.Ceshi_class at 0x103b4eae0 > ,
	'root_path': '/private/tmp',
	'__builtins__': < module '__builtin__' (built - in ) > ,
	'__file__': 'command.py',
	'inspect': < module 'inspect' from 'xxx/python2.7/inspect.pyc' > ,
	'__doc__': None,
	'sys': < module 'sys' (built - in ) > ,
	'_usage': < function _usage at 0x103c02aa0 > ,
	'time': < module 'time' from 'xxx/python2.7/lib-dynload/time.so' > ,
	'__name__': '__main__',
	'__package__': None,
	'os': < module 'os' from 'xxx/python2.7/os.pyc' > ,
	'hello': < function hello at 0x103b70668 >
}
```
获取可用的函数和类
> * globals() 中判断是否为函数：inspect.isfunction(v)
> * globals() 中判断是否为类：inspect.isclass(v)
>   * 类中根据 v.__dict__ 判断是否有 staticmethod 或者 classmethod

v.__dict__ 内容如下
```
{
	'__module__': '__main__',
	'ceshi_func2': < staticmethod object at 0x1039d1590 > ,
	'__doc__': None,
	'ceshi_func1': < classmethod object at 0x1039d1558 >
}
```
备注：类中的 staticmethod 和 classmethod ，使用 inspect.isfunction() 判断时为 False, 所以使用 str 进行匹配判断

#### 2.2.2 获取函数的参数

todo
