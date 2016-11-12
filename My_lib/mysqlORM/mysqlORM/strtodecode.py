#!/usr/bin/python
#-*- coding:utf-8 -*-
"""编码检测及转换为unicode
@since:2014/07/28
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("..")
import chardet

def strtodecode(s=''):			#编码检测及转换为unicode
	if not s:
		return False

	tempstr = s
	try:
		chardetdict = chardet.detect(tempstr)
	except:
		pass
	else:
		try:
			if tempstr.decode('utf-8','ignore').encode('utf-8') == tempstr:
				templabelstrdecode = tempstr.decode('utf-8','ignore').encode('utf-8').decode('utf-8')
			elif tempstr.decode('gbk','ignore').encode('gbk') == tempstr:
				templabelstrdecode = tempstr.decode('gbk','ignore').encode('utf-8').decode('utf-8')
			else:
				templabelstrdecode = tempstr.decode(chardetdict['encoding'],'ignore').encode('utf-8').decode('utf-8')
		except:
			pass
		else:
			tempstr = templabelstrdecode

	return tempstr
