#!/usr/bin/python
#coding=utf8
 
from mylib.snack_lib import *
 
screen = SnackScreen()
###############################
# 1 级菜单
###############################
def main():
    m = Mask( screen, "运维工具", 35 )
    #m.entry( "Entry", "entry1", "value of entry 1" )
    #m.password( "Password", "passwd1", "value of entry 1" )
    #m.radios( "Select", "sel1", [ ('Yes','yes', 0), ('No','no', 1) ] )
    m.list( "List", "list1", [ ('管理1','wp', 0), ('管理2','crontab', 1),('管理3','service', 1) ] )
    #m.checks( "Check", "chk1", [ ('Yes','yes', 0), ('No','no', 1) ] )
    m.buttons( yes="Yes", no="No" )
    #m.buttons( yes="Yes")
    (cmd, results) = m.run()
    if cmd == "yes":
        if results['list1'] == "wp":
            wp()
        #www()

###############################
# 2 级菜单
###############################

def wp():
    m = Mask( screen, "www", 35 )
    #m.entry( "Entry", "entry1", "value of entry 1" )
    #m.password( "Password", "passwd1", "value of entry 1" )
    #m.radios( "Select", "sel1", [ ('Yes','yes', 0), ('No','no', 1) ] )
    m.list( "List", "list2", [ ('server1','server1', 0), ('server2','server2', 1),('server3','server3', 1)  ] )
    #m.checks( "Check", "chk1", [ ('Yes','yes', 0), ('No','no', 1) ] )
    m.buttons( yes="Yes", no="No" )
    #m.buttons( yes="Yes")
    (cmd, results) = m.run()
    if cmd == "yes":
        if results['list2'] == "server1":
            warwindows(screen, "说明", "只是说一句话")
            server1()
 
###############################
# 3 级菜单
###############################
def server1():
    m = Mask( screen, "server1", 35 )
    m.entry( "端口", "port", "80" )
    #m.password( "Password", "passwd1", "value of entry 1" )
    #m.radios( "Select", "sel1", [ ('Yes','yes', 0), ('No','no', 1) ] )
    #m.list( "List", "list2", [ ('xserver','xserver', 0), ('unode','unode', 1),('uctr','uctr', 1)  ] )
    #m.checks( "Check", "chk1", [ ('Yes','yes', 0), ('No','no', 1) ] )
    m.buttons( yes="Yes", no="No" )
    #m.buttons( yes="Yes")
    (cmd, results) = m.run()
    #print cmd,results
    #if cmd == "yes":
    #    if results['list2'] == "xserver":
    #        wp()
    return 0

main()
screen.finish()
#print cmd, results

# will print something like:
# yes {'passwd1': 'value of entry 1', 'entry1': 'Value of the entry', 'list1': 'no', 'sel1': 'no', 'chk1': ['no']}
