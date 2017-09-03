#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2017-08-31 16:09:18

# File Name: wwww.py
# Description:

"""
import urllib2
  
url = 'http://xxxx.cm/ping'
response = None
try:
  response = urllib2.urlopen(url,timeout=3)
  print "xxxxxxxxx"
except urllib2.URLError as e:
  if hasattr(e, 'code'):
    print 'Error code:',e.code
  elif hasattr(e, 'reason'):
    print 'Reason:',e.reason

#print response.code
