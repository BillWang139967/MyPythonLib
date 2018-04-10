#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2018-04-10 23:23:55

# File Name: demo1.py
# Description:

"""
from w_lib.mpms import MPMS
import random
import time

def worker(i, j=None):
    time.sleep(3)
    return i,j

def main():
    m = MPMS(
        worker,
        processes=2,
        threads=100,  # 每进程的线程数
    )
    m.start()
    for i in range(200):  # 你可以自行控制循环条件
        m.put(i, random.randint(0,99))  # 这里的参数列表就是worker接受的参数
    m.join()
    result = m.get_result()
    print result

if __name__ == '__main__':
    main()
