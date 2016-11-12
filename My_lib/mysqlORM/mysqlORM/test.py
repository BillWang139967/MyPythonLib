#!/usr/bin/python
#-*- coding:utf-8 -*-
#在config.py里配置数据库连接
from mysql_conn import myMdb

mydb = myMdb()

#新建表结构
mydb.setTable('testtablename',
			"(`test_id` int(10) NOT NULL AUTO_INCREMENT,`test_col1` varchar(255) NOT NULL,`test_col2` varchar(255) NOT NULL, PRIMARY KEY (`test_id`), KEY `test_col1` (`test_col1`), KEY `test_col2` (`test_col2`)) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;"
			)

#新增数据记录
tag = mydb._insert({'test_col1':'123','test_col2':'455'})._from('testtablename').execute()
print tag

#修改数据记录
tag = mydb._update({'test_col2':'456'})._from('testtablename')._where({'column':'test_id','data':'1','relation':'='}).execute()
print tag

#删除数据记录
tag = mydb._delete()._from('testtablename')._where({'column':'test_id','data':'3','relation':'<'}).execute()
print tag

#查询前100条数据并排序
rs = mydb._select('*')._from('testtablename')._where({'column':'test_col1','data':'123','relation':'='})._where({'column':'test_col2','data':'456','relation':'!='})._limit(100,1)._order({'test_id':'DESC'}).execute()
print rs

#两表联合查询
#rs = mydb._select('a.*')._from('testtablename_1','a')._leftjoin('testtablename_2','b','a.test_col1=b.test_col1')._where({'column':'a.test_col1','data':'123','relation':'='}).execute()
#print rs

#支持上下文管理方式调用
with myMdb() as mydb:
	tag = mydb._insert({'test_col1':'123','test_col2':'455'})._from('testtablename').execute()
print tag

#打印调试最近一次执行的sql语句
print mydb.getsql
