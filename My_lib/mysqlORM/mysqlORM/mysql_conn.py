#!/usr/bin/python
#-*- coding:utf-8 -*-

"""封装的mysql ORM模型类
@version:1.5
@see: https://pypi.python.org/pypi/MySQL-python
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("..")
import MySQLdb as mdb
import simplejson as json
import config as config				#配置文件
from strtodecode import strtodecode	#编码


def typeValuetoStr(s):			#对数据库入库字段值格式化
	if not s:
		return s

	decode_s,dump_s = '',''
	if isinstance(s, str):		#检测str编码并转成unicode
			try:
				json.loads(s)
			except:
				decode_s = strtodecode(s)
			else:
				decode_s = s 							#json的结果直接存数据库

	elif isinstance(s, unicode):
			decode_s = strtodecode(s)
	else:												#非str类型的先转成json格式
		dump_s = json.dumps(s)

	if decode_s:										#转unicode成功
		try:
			rs = decode_s.encode(config.mysql_charset)
		except:
			return decode_s.encode('utf8').replace('\\','\\\\')	#对数据库指定编码转码失败返回默认utf8编码
		else:
			return rs.replace('\\','\\\\')
	elif dump_s:												#转unicode失败
		return dump_s.replace('\\','\\\\')
	else:
		return False

class myMdb(object):
	def __init__(self):
		self.con = mdb.connect(host=config.mysql_host, user=config.mysql_user, passwd=config.mysql_passwd, db=config.mysql_db, charset=config.mysql_charset)
		self.cur = self.con.cursor(mdb.cursors.DictCursor)
		self.fromlist = []
		self.wherelist = []
		self.deletelist = []
		self.selectlist = []
		self.orderlist = []
		self.limitlist = []
		self.updatelist = []
		self.inslist = []
		self.leftjoinlist = []
		self.selectas = ''
		self.selectas_b = ''
		self.sql = ''
		self.withtag = False

	def __del__(self):
		if not self.withtag:
			self.cur.close()
			self.con.commit()
			self.con.close()

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.cur.close()
		self.con.commit()
		self.con.close()

	def __enter__(self):
		self.withtag = True
		return self

	def __assemble(self):
		if self.selectlist and (self.deletelist or self.updatelist or self.inslist):
			raise Exception('sql error')
			return False
		if self.deletelist and self.updatelist:
			raise Exception('sql error')
			return False
		if self.deletelist and self.inslist:
			raise Exception('sql error')
			return False
		if self.updatelist and self.inslist:
			raise Exception('sql error')
			return False

		wherestr = 'where '
		if self.wherelist:
			for i in xrange(0,len(self.wherelist)):
				relation_temp = self.wherelist[i].get('relation',False)
				if (self.wherelist[i].get('column',False) != None):
					column_temp = str(self.wherelist[i]['column'])
				if (self.wherelist[i].get('data', None) != None):
					data_temp = str(self.wherelist[i]['data'])
				if column_temp and data_temp and relation_temp:

					if self.selectas:
						column_temp_truple = column_temp.split('.')
						data_temp_truple = data_temp.split('.')
						if len(column_temp_truple) < 2:		#错误
							self.__reset()					#重置所有全局参数
							raise Exception('sql error')
							return False
						if i > 0:
							if self.selectas_b:
								if len(data_temp_truple) > 1 and (data_temp_truple[0]==self.selectas or data_temp_truple[0]==self.selectas_b):
									wherestr += "and `{0}`.`{1}` {2} `{3}`.`{4}` ".format(column_temp_truple[0],column_temp_truple[1],relation_temp,data_temp_truple[0],data_temp_truple[1])
								else:
									wherestr += "and `{0}`.`{1}` {2} '{3}' ".format(column_temp_truple[0],column_temp_truple[1],relation_temp,data_temp)
						else:
							if self.selectas_b:
								if len(data_temp_truple) > 1 and (data_temp_truple[0]==self.selectas or data_temp_truple[0]==self.selectas_b):
									wherestr += "`{0}`.`{1}` {2} `{3}`.`{4}` ".format(column_temp_truple[0],column_temp_truple[1],relation_temp,data_temp_truple[0],data_temp_truple[1])
								else:
									wherestr += "`{0}`.`{1}` {2} '{3}' ".format(column_temp_truple[0],column_temp_truple[1],relation_temp,data_temp)
					else:
						if i > 0:
							wherestr += "and `{0}` {1} '{2}' ".format(column_temp, relation_temp, typeValuetoStr(data_temp))
						else:
							wherestr += "`{0}` {1} '{2}' ".format(column_temp, relation_temp, typeValuetoStr(data_temp))
			if wherestr == 'where ':
				raise Exception("format where sql error:need {'column':'','data':'','relation':''}")
				wherestr = ''
		if wherestr == 'where ':
			wherestr = ''

		selectstr,deletestr,updatestr,insstr = '','','',''
		if self.selectlist:
			selectstr += "select {0} ".format(b",".join(self.selectlist))
		elif self.deletelist:
			deletestr += "delete "
		elif self.updatelist:
			updatestr = self.__update()
		elif self.inslist:
			insstr = self.__insert()

		if (not wherestr) and updatestr:
			raise Exception('need where parts')
			return False

		fromstr = ''
		if not self.fromlist:
			raise Exception('from table can not be None')
			return False
		else:
			if self.leftjoinlist and self.selectas:
				fromstr += 'from `{0}` as `{1}` '.format(self.fromlist[0], self.selectas)
			else:
				fromstr += 'from `{0}` '.format(self.fromlist[0])
		if not fromstr:
			return False
		elif updatestr or insstr:
			fromstr = ''

		leftjoinstr = ''
		if self.leftjoinlist:
			jtable = self.leftjoinlist[0].get('table', False)
			jasname = self.leftjoinlist[0].get('asname', False)
			jon = self.leftjoinlist[0].get('on', False)
			if jtable and jasname and jon:
				leftjoinstr += 'left join `{0}` as `{1}` on {2} '.format(jtable, jasname, jon)

		orderstr = 'order by '
		if self.orderlist:
			for i in xrange(0,len(self.orderlist)):
				for key,value in self.orderlist[i].iteritems():
					valueTemp = value.upper()
					if valueTemp == 'DESC' or valueTemp == 'ASC':
						value = valueTemp
					else:
						continue
					if i > 0:
						orderstr += ",`{0}` {1} ".format(key, value)
					else:
						orderstr += "`{0}` {1} ".format(key, value)
		if orderstr == 'order by ':
			orderstr = ''

		limitstr = ''
		if self.limitlist:
			limitstr += "limit {0},{1} ".format(self.limitlist[0][0], self.limitlist[0][1])

		self.sql = selectstr + deletestr + updatestr + insstr + fromstr + leftjoinstr + wherestr + orderstr + limitstr
		if self.sql:
			return self.__execute(self.sql)
		else:
			return False

	def __execute(self, sql=''):
		if not sql:
			return False

		try:
			tag = self.cur.execute(sql)
		except:
			print "sql error:%s" % sql

		if tag:
			if self.selectlist:
				rows = self.cur.fetchall()
				if rows:
					self.__reset()			#重置所有全局参数
					return rows
			elif self.inslist:
				self.__reset()				#重置所有全局参数
				return self.cur.lastrowid
			else:
				self.__reset()				#重置所有全局参数
				return tag

		self.__reset()						#重置所有全局参数
		return tag

	def __update(self):
		set_field = ''
		if self.updatelist:
			for i in xrange(0,len(self.updatelist)):
				if i > 0:
					set_field += ',' + b",".join(map(lambda x:"`%s` = \'%s\'" % (x[0],typeValuetoStr(x[1])), self.updatelist[i].iteritems()))
				else:
					set_field += b",".join(map(lambda x:"`%s` = \'%s\'" % (x[0],typeValuetoStr(x[1])), self.updatelist[i].iteritems()))

		if set_field:
			return "UPDATE `{0}` SET {1} ".format(self.fromlist[0], set_field)
		else:
			return ''

	def __getTypeValue(self, i, ins_key):
		ins_val = self.inslist[i].get(ins_key, None)
		if ins_val != None:
			return '\"%s\"' % typeValuetoStr(str(ins_val)).replace('"','\'')
		else:
			return 'NULL'

	def __insert(self):
		value_field = ''
		key_field = ''
		if self.inslist:
			for i in xrange(0,len(self.inslist)):
				key_list = sorted(list(self.inslist[i].iterkeys()))					#格式化sql操作字段
				value_list = map(lambda x: self.__getTypeValue(i,x), key_list)
				value_field_temp = ''
				try:
					key_field = b",".join(map(lambda x:"`%s`" % x, key_list))
					value_field_temp = "(" + b",".join(value_list) + ")"
				except:
					raise Exception("insert Type error")
					return False 							#入库字段异常直接退出

				if i > 0:
					value_field += "," + value_field_temp
				else:
					value_field += value_field_temp

		if value_field:
			return "INSERT INTO `{0}` ({1}) VALUES {2} ".format(self.fromlist[0], key_field, value_field)
		else:
			return ''

	def __reset(self):
		self.fromlist = []
		self.wherelist = []
		self.deletelist = []
		self.selectlist = []
		self.orderlist = []
		self.limitlist = []
		self.updatelist = []
		self.inslist = []
		self.leftjoinlist = []
		self.selectas = ''
		self.selectas_b = ''

	def execute(self):
		return self.__assemble()

	@property
	def getsql(self):
		return self.sql

	#update_data = {'字段名':'数据','字段名':'数据'}
	def _update(self,update_data={}):
		if not update_data:
			return False
		self.updatelist.append(update_data)
		return self

	#ins_data = {'字段名':'数据','字段名':'数据'}
	def _insert(self,ins_data={}):
		if not ins_data:
			return False
		self.inslist.append(ins_data)
		return self

	#search_data={'column':'字段名','data':'字段值','relation':'关系'}
	def _where(self, search_data={}):
		if not search_data:
			raise Exception('search can not be None')
			return False
		self.wherelist.append(search_data)
		return self

	def _from(self, table='', asname=''):
		if not table:
			raise Exception('from table can not be None')
			return False
		self.fromlist.append(table)

		if asname:
			self.selectas = asname

		return self

	def _delete(self):
		self.deletelist = []
		self.selectlist = []
		self.deletelist = ['delete']
		return self

	def _select(self, str="*"):
		if not str:
			raise Exception('str can not be None')
			return False
		self.deletelist = []
		self.selectlist.append(str)

		return self

	#order_data = {'column':'desc/asc'}
	def _order(self, order_data = {}):
		if not order_data:
			raise Exception('order can not be None')
			return False
		self.orderlist.append(order_data)
		return self

	def _limit(self, limits=100, offsets=0):
		if not isinstance(offsets, int):
			raise Exception('offset should be int')
			return False
		if not limits:
			raise Exception('limit can not be None')
			return False
		if not isinstance(limits, int):
			raise Exception('type limit error')
			return False
		self.limitlist.append([offsets, limits])
		return self

	#table 表名  asname别名名称  on: a.field = b.field
	def _leftjoin(self, table='', asname='', on=''):
		if not table:
			raise Exception('leftjoin table can not be None')
			return False
		if not asname:
			raise Exception('leftjoin as name can not be None')
			return False
		if not on:
			raise Exception('leftjoin on relation can not be None')
		self.leftjoinlist.append({'table':table, 'asname':asname, 'on':on})
		self.selectas_b = asname
		return self


	#creat table
	def setTable(self, table_name='', table_struc=''):
		if not table_name:
			return False
		if not table_struc:
			return False
		try:
			sql = "create table if not exists `%s` %s" % (strtodecode(table_name), strtodecode(table_struc))
			self.sql = sql
			tag = self.cur.execute(sql)
		except:
			print "sql error:%s" % sql
		else:
			return tag

