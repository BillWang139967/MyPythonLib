#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2017-09-01 15:42:47

# File Name: ceshi.py
# Description:

"""
import time

def ceshi():
    while True:
        print "helloworld"
        print "Start : %s" % time.ctime()
        time.sleep(1)
        print "End : %s" % time.ctime()
if __name__ == "__main__":
    ceshi()
