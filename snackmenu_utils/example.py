#!/usr/bin/python
#coding=utf8
 
from mylib.snack_lib import *

screen = SnackScreen()
def test():
     m = Mask( screen, "test_windows", 35 )
     m.entry( "label_test1", "entry_test1", "0" )
     m.entry( "label_test2", "entry_test2", "0" )
     m.entry( "label_test3", "entry_test3", "127.0.0.1" )
     m.checks( "复选框","checks_list",[
         ('checks_name1','checks1',0),
         ('checks_name2','checks2',0),
         ('checks_name3','checks3',0),
         ('checks_name4','checks4',1),
         ('checks_name5','checks5',0),
         ('checks_name6','checks6',0),
         ('checks_name7','checks7',0),
     ],
     height= 5
     )    
     m.radios( "单选框","radios", [ 
         ('radios_name1','radios1', 0), 
         ('radios_name2','radios2', 1), 
         ('radios_name3','radios3', 0) ] )  
     
     m.buttons( ok="Sava&Quit", cancel="Quit" )
     #(cmd, results) = m.run(12,3)
     (cmd, results) = m.run()
     screen.finish() 
     return cmd,results

(cmd,results) = test()
print cmd,results
