#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2017-09-03 23:27:32

# File Name: wwwb.py
# Description:

"""
import urllib2  
  
url     = "http://xxxxx.com/xxx"  
try:  
    response = urllib2.urlopen(url,timeout=3)  
    # print response.read( )  
    response.close( )  
    # HTTPError必须排在URLError的前面  
    # 因为HTTPError是URLError的子类对象  
    # 在网访问中引发的所有异常要么是URLError类要么是其子类  
    # 如果我们将URLError排在HTTPError的前面，那么将导致HTTPError异常将永远不会被触发  
    # 因为Python在捕获异常时是按照从前往后的顺序挨个匹配的  
    print "xxxxxx"
except urllib2.HTTPError, e:  
    print "The server couldn't fulfill the request"  
    print "Error code:", e.code  
    if e.code == 404:  
        print "Page not found!"  
        #do someting  
    elif e.code == 403:  
        print "Access denied!"  
        #do someting  
    else:  
        print "Something happened! Error code", e.code  
    #print "Return content:", e.read()  
except urllib2.URLError, e:  
    print "Failed to reach the server"  
    print "The reason:", e.reason 
