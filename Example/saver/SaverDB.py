import sys, os
import MySQLdb as mysql
import json
import hashlib
from netlib.NetBase import nbNet

monTables = [
            'stat_0',
            'stat_1',
            'stat_2',
            'stat_3',
            ]

db = mysql.connect(user="root", passwd="123456",charset="utf8")
cur = db.cursor()
#db.autocommit(True)
try:
    cur.execute('create database dbtest')
except:
    print 'Database dbtest exists!'

db.select_db('dbtest')
try:
    for i in range(4): 
        sql = "CREATE TABLE `stat_%d` (`host` char(20),`mem_free` \
        int(10),`mem_usage` int(10),`mem_total` int(10),`load_avg` \
        char(20),`time` int(20))" %i
        cur.execute(sql)
except:
    print 'TABLE exists'

def fnvhash(string):
    ret = 97
    for i in string:
        ret = ret ^ ord(i) * 13
    return ret

def insertMonData(mondata):
    try:
        data = json.loads(mondata)
        timeOfData = int(data['Time'])
        hostIndex = monTables[fnvhash(data['Host']) % len(monTables)]
        sql = "insert into `%s`  (`host`,`mem_free`,`mem_usage`,`mem_total`,`load_avg`,`time`) VALUES('%s', '%d', '%d', '%d', '%s', '%d')" % \
            (hostIndex, data['Host'], data['MemFree'], data['MemUsage'], data['MemTotal'], data['LoadAvg'], timeOfData)
        ret = cur.execute(sql)
    except mysql.IntegrityError:
        pass
    
def logic(d_in):   
    insertMonData(d_in)
    return "OK"
def start():
    saverD = nbNet('0.0.0.0', 50003, logic)
    saverD.run()

if __name__ ==  "__main__":
    start()
    



