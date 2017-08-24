#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2017-08-24 17:29:17

# File Name: command_class.py
# Description:

"""
from __future__ import print_function

class ceshi_class():

    '''ceshi'''

    def output(self, str_info):
        '''eg:python command_class.py output "hello world"'''
        print('hello %s' % str_info)
    def output2(self, str_info="happy"):
        '''eg:python command_class.py output2 "hello world"'''
        print('hello %s' % str_info)

if __name__ == '__main__':
    import os
    from pydoc import render_doc
    import argparse
    # Handle command-line options
    ceshi= ceshi_class()
    parser=argparse.ArgumentParser(usage='\033[43;37mpython %(prog)s function param [options]\033[0m')
    #parser.add_argument("-c", "--config", dest="config", default=os.environ['HOME'] + '/.config',
    #                  help="CONFIG file", metavar="CONFIG")
    #parser.add_argument("-s", "--section", dest="section", default='default',
    #                  help="Section of config file to use file", metavar="SECTION")
    options, unknown_args = parser.parse_known_args()
    options = vars(options)

    # options 命令行参数
    # print(options)

    # unknown_args 是类中的方法以及方法所需的参数(第一个值为类中的方法)
    # print(unknown_args)

    # 如果没有调用类中的方法
    if not unknown_args:
        print(parser.print_help())
        print(render_doc(ceshi_class))
        exit()

    func = unknown_args.pop(0)
    try:
        cmd = getattr(ceshi, func)
    except:
        print('No such function: %s' % func)
        print(render_doc(ceshi_class))
        exit()
    try:
        kwargs = {}
        func_args = []
        for arg in unknown_args:
            if '=' in arg:
                key, value = arg.split('=', 1)
                kwargs[key] = value
            else:
                func_args.append(arg)
        func_args = tuple(func_args)

        # 此步执行程序
        function_result = cmd(*func_args, **kwargs)
    except TypeError:
        print(render_doc(cmd))
        exit()
