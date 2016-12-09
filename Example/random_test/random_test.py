#!/usr/bin/python
#coding=utf-8
"""
# Author: meetbill
# Created Time : 2016-12-08 22:38:08

# File Name: random_test.py
# Description: 随机选择一道题，并且随机选择一个人进行作答

"""
import linecache
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def test():
    f = [ x.replace('\n','') for x in linecache.getlines('doc/test.txt')]
    random_int = random.randint(0, len(f)-1)
    return f[random_int]

def user():
    f = [ x.replace('\n','') for x in linecache.getlines('doc/user.txt')]
    random_int = random.randint(0, len(f)-1)
    return f[random_int]
          
print('嘿嘿，开始选择今天的幸运使者:' )
print """
////////////////////////////////////////////////////////////////////  
//                            _ooOoo_                             //  
//                           o8888888o                            //      
//                           88" . "88                            //      
//                           (| -_- |)                            //      
//                           O\  =  /O                            //  
//                        ____/`---'\____                         //                          
//                      .'  \\|     |//  `.                       //  
//                     /  \\|||  :  |||//  \                      //      
//                    /  _||||| -:- |||||-  \                     //  
//                    |   | \\\  -  /// |   |                     //  
//                    | \_|  ''\---/''  |   |                     //          
//                    \  .-\__  `-`  ___/-. /                     //          
//                  ___`. .'  /--.--\  `. . ___                   //      
//                ."" '<  `.___\_<|>_/___.'  >'"".                //  
//              | | :  `- \`.;`\ _ /`;.`/ - ` : | |               //      
//              \  \ `-.   \_ __\ /__ _/   .-` /  /               //  
//        ========`-.____`-.___\_____/___.-`____.-'========       //      
//                             `=---='                            //  
//        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^      //  
//                         寻找有缘人                             //  
//////////////////////////////////////////////////////////////////// 

"""
print "题目:",test()
print
print "幸运者:",user()
