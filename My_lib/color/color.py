#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2018-07-13 23:31:15

# File Name: color.py
# Description:

"""
"""
格式：\033[显示方式;前景色;背景色m

说明：
前景色            背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              紫红色
36                46              青蓝色
37                47              白色

显示方式           意义
-------------------------
0                终端默认设置
1                高亮显示
4                使用下划线
5                闪烁
7                反白显示
8                不可见
"""


def colored(text, color=None, on_color=None, attrs=None):
    fmt_str = '\x1B[;%dm%s\x1B[0m'
    if color is not None:
        text = fmt_str % (color, text)

    if on_color is not None:
        text = fmt_str % (on_color, text)

    if attrs is not None:
        for _ in attrs:
            text = fmt_str % (color, text)

    return text


def print_error(msg):
    print colored(msg, color=31)


def print_warning(msg):
    print colored(msg, color=33)


def print_info(msg):
    print colored(msg, color=32)


def print_log(msg):
    print colored(msg, color=35)


def print_debug(msg):
    print colored(msg, color=36)


def color_print(msg, level='info'):
    color_print_dict = {
        "error": print_error,
        "info": print_info,
        "log": print_log,
        "warning": print_warning,
        "debug": print_debug
        # add more
    }
    if level in color_print_dict:
        color_print_dict[level](msg)
    else:
        print msg


if __name__ == '__main__':
    # test
    print_error("this is an error message!")
    print_warning("this is a warning message!")
    print_info("this ia a info message!")
    print_log('this is a log message!')
    print_debug('this is a debug message!')
    color_print('test info message!', 'info')
