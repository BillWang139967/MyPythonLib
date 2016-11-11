#!/usr/bin/python
#coding=utf8
"""
# Author: 遇见王斌
# Created Time : 2016-11-11 22:39:02

# File Name: ww.py
# Description:

"""
import subprocess
def check(p_name):
    cmd = 'ps -ef |grep %s|grep -v "grep"' % p_name
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    if p.wait() == 0:
        val = p.stdout.read()
        if p_name in val:
              print "running"
    else:
        print "no running"


check("unode")

