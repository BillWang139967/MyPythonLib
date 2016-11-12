#-*- coding:utf-8 -*-
from inspect import currentframe
import socket
import select
import time

DEBUG = False

#{{{get_linenumber
def get_linenumber():
    cf = currentframe()
    return str(cf.f_back.f_back.f_lineno)
#}}}

#{{{dbgPrint
def dbgPrint(msg):
    if DEBUG:
        print get_linenumber(), msg
#}}}

import signal, functools

class TimeoutError(Exception):pass

#{{{timeout
def timeout(seconds, error_message="function call time out"):
    
    def decorated(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message);
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(10)
                return result
        return functools.wraps(func)(wrapper)
    return decorated
#}}}

@timeout(5)
#{{{connect_timeout
def connect_timeout(socket, host_port):
    return socket.connect(host_port)
#}}}
#{{{sendData_mh
def sendData_mh(sock_list, host_list, data, single_host_retry=3):
    """
    saver_list = [host1:port, host2:port, host3:port]
    sock_list = [some socket]
    """
    done = False
    for host_port in host_list:
        if done:
            break
        host, port = host_port.split(":")
        port = int(port)
        retry = 0
        while retry < single_host_retry:
            try:
                if sock_list[0] == None:
                    sock_list[0] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock_list[0].settimeout(5)
                    sock_list[0].connect((host, port))
                d = data
                sock_list[0].sendall("%010d%s" % (len(d), d))
                count = sock_list[0].recv(10)
                if not count:
                    raise Exception("recv error")
                count = int(count)
                buf = sock_list[0].recv(count)
                if buf[:2] == "OK":
                    retry = 0
                    break
                
            except:
                sock_list[0].close()
                sock_list[0] = None
                retry += 1
#}}}
#{{{sendData
def sendData(sock_l, host, port, data):               
    retry = 0
    while retry < 3:
        try:
            if sock_l[0] == None:
                sock_l[0] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_l[0].connect((host, port))
                dbgPrint("\n-- start connect %s:%d" %(host, port))
            d = data
            sock_l[0].sendall("%010d%s" %(len(data), data))
            count = sock_l[0].recv(10)
            if not count:
                raise Exception("recv error")
            buf = sock_l[0].recv(int(count))
            dbgPrint("recv data: %s" % buf)
            if buf[:2] == "OK":
                retry = 0
                break
        except:
            sock_l[0].close()
            sock_l[0] = None
            retry += 1
#}}}           
# initial status for state machine
#{{{STATE
class STATE:
    def __init__(self):
        self.state = "accept"
        self.have_read = 0
        self.need_read = 10
        self.have_write = 0
        self.need_write = 0
        self.buff_write = ""
        self.buff_read = ""
        # sock_obj is a object
        self.sock_obj = ""

    def printState(self):
        if DEBUG:
            dbgPrint('\n - current state of fd: %d' % self.sock_obj.fileno())
            dbgPrint(" - - state: %s" % self.state)
            dbgPrint(" - - have_read: %s" % self.have_read)
            dbgPrint(" - - need_read: %s" % self.need_read)
            dbgPrint(" - - have_write: %s" % self.have_write)
            dbgPrint(" - - need_write: %s" % self.need_write)
            dbgPrint(" - - buff_write: %s" % self.buff_write)
            dbgPrint(" - - buff_read:  %s" % self.buff_read)
            dbgPrint(" - - sock_obj:   %s" % self.sock_obj)
#}}}
