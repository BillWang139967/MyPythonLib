#!python

from Queue import Queue
import time
import socket
import sys, os
import threading
import json

from netlib.NetBase import nbNet
from netlib.NetUtils import sendData
from monitems import Mon

class porterThread(threading.Thread):
    
    def __init__(self, name, queue, interval=None, host=None, port=None):
        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.interval = interval
        self.host = host
        self.port = port
        
    def run(self):
        if self.name == 'collect':
            self.collect_data()
        elif self.name == 'senddata':
            self.send_data()
        elif self.name == 'receivecmd':
            self.receivecmd()
        elif self.name == 'sendcmdresult':
            self.sendcmdresult()
        
    def collect_data(self):
        m = Mon()
        atime = int(time.time())
        while 1:
            data = m.runAllGet()
            self.queue.put(data)
            btime = int(time.time())
            time.sleep(self.interval-((btime-atime)%self.interval))
    def send_data(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_l = [s]
            s.connect((self.host, self.port))
        except socket.error as err:
            print err
        while 1:
            print "send data to %s %s" %(self.host, self.port)
            if not self.queue.empty():
                data = self.queue.get()
                sendData(sock_l, self.host, self.port, json.dumps(data))
                print data, "q size is: ", self.queue.qsize()
            time.sleep(self.interval)

    def receivecmd(self):
        pass

    def sendcmdresult(self):
        pass

        

def startTh():
    queue = Queue(10)
    collect = porterThread("collect", queue, interval=30)
    collect.start()
    time.sleep(0.5)  # why must sleep
    senddata = porterThread("senddata", queue, interval=30, host="127.0.0.1",port=50003)
    senddata.start()
    #cmdqueue = Queue(10)
    #recvcmd = porterThread("receivecmd", cmdqueue, interval=30, host="0.0.0.0", port=50000)
    #recvcmd.start()
    #sendcmdresult = porterThread("sendcmdresult", cmdqueue, interval=30,host = '0.0.0.0', port=50002)
    #sendcmdresult.start()
    
    collect.join()
    senddata.join()
    #recvcmd.join()
    #sendcmdresult()
    
if __name__ == '__main__':
    startTh()
