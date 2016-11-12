#-*- coding:utf-8 -*-
from daemon import Daemon
import socket
import select
import time

from NetUtils import dbgPrint

__all__ = ["nbNet", "sendData_mh"]

#DEBUG = True
from NetUtils import *

class nbNetBase:
    def setFd(self, sock):
        """sock is class object of socket"""
        dbgPrint("\n -- setFd start!")
        _state = STATE()
        _state.sock_obj = sock
        self.conn_state[sock.fileno()] = _state
        self.conn_state[sock.fileno()].printState()
        dbgPrint("\n -- setFd End!")
        
    def accept(self, fd):
        dbgPrint("\n -- start Accept function")
        _sock_state = self.conn_state[fd]
        _sock = _sock_state.sock_obj
        conn, addr = _sock.accept()
        conn.setblocking(0)
        return conn
    
    
    def close(self, fd):
        try:
            sock = self.conn_state[fd].sock_obj
            sock.close()
            self.epoll_sock.unregister(fd)
            self.conn_state.pop(fd)
        except:
            dbgPrint("Close fd: %s abnormal" % fd)
            pass
        
    def read(self,fd):
        try:
            sock_state = self.conn_state[fd]
            conn = sock_state.sock_obj
            if sock_state.need_read <= 0:
                raise socket.error
            one_read = conn.recv(sock_state.need_read).lstrip()
            dbgPrint("\tread func fd %d,  one_read: %s, need_read: %d" %(fd, one_read, sock_state.need_read))
            if len(one_read) == 0:
                raise socket.error
            sock_state.buff_read += one_read
            sock_state.have_read += len(one_read)
            sock_state.need_read -= len(one_read)
            sock_state.printState()
            
            if sock_state.have_read == 10:
                header_said_need_read = int(sock_state.buff_read)
                print "header_said_need_read %d" % header_said_need_read
                if header_said_need_read <= 0:
                    raise socket.error
                sock_state.need_read += header_said_need_read
                sock_state.buff_read=""
                sock_state.printState()
                return "readcontent"
            elif sock_state.need_read == 0:
                return "process"
            else:
                return "readmore"
        except (socket.error, ValueError) , msg:
            try:
                if msg.error == 11:
                    dbgPrint("11 " + msg)
                    return "retry"
            except:
                pass
            return 'closing'
        
        
    def write(self, fd):
        sock_state = self.conn_state[fd]
        conn = sock_state.sock_obj
        last_have_send = sock_state.have_write
        try:
            have_send = conn.send(sock_state.buff_write[last_have_send:])
            sock_state.have_write += have_send
            sock_state.need_write -= have_send
            if sock_state.need_write == 0 and sock_state.have_write != 0:
                conn.send("0000000002OK")    #此处真坑爹啊！ 调试一天发现的问题
                dbgPrint("\n write data completed!")
                return "writecomplete"
            else:
                return "writemore"
        except socket.error, msg:
            return "closing"
        
    def run(self):
        while True:
            dbgPrint("\n -- run func loop")
            for i in self.conn_state.iterkeys():
                dbgPrint("\n -- state of fd: %d" % i)
                self.conn_state[i].printState();
                
            epoll_list = self.epoll_sock.poll()
            for fd, events in epoll_list:
                dbgPrint("\n-- run epoll return fd: %d, event: %s" %(fd, events))
                sock_state = self.conn_state[fd]
                if select.EPOLLHUP & events:
                    dbgPrint("events EPOLLHUP")
                    sock_state.state = "closing"
                elif select.EPOLLERR & events:
                    dbgPrint("EPOLLERROR")
                    sock_state.state = "closing"
                    
                self.state_machine(fd)

    def state_machine(self, fd):
        dbgPrint("\n-- state machine: fd %d, statue is: %s" %(fd, self.conn_state[fd].state))
        sock_state = self.conn_state[fd]
        self.sm[sock_state.state](fd)
        
class nbNet(nbNetBase):
    def __init__(self, addr, port, logic):
        dbgPrint("\n-- __init__: start!")
        self.conn_state = {}
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_sock.bind((addr, port))
        self.listen_sock.listen(10)
        self.setFd(self.listen_sock)
        self.epoll_sock = select.epoll()
        self.epoll_sock.register(self.listen_sock.fileno(), select.EPOLLIN)
        self.logic = logic
        self.sm = {
                   'accept': self.accept2read,
                   "read": self.read2process,
                   "write":self.write2read,
                   "process": self.process,
                   "closing": self.close,
                   }
        
    def process(self, fd):
        sock_state = self.conn_state[fd]
        response = self.logic(sock_state.buff_read)
        sock_state.buff_write = "%010d%s" %(len(response), response)
        dbgPrint("%010d%s" %(len(response), response))
        sock_state.need_write = len(sock_state.buff_write)
        sock_state.state = "write"
        self.epoll_sock.modify(fd, select.EPOLLOUT)
        sock_state.printState()
        
    def accept2read(self, fd):
        conn = self.accept(fd)
        self.epoll_sock.register(conn.fileno(), select.EPOLLIN)
        self.setFd(conn)
        self.conn_state[conn.fileno()].state = "read"
        
    def read2process(self, fd):
        read_ret = ""
        try:
            read_ret = self.read(fd)
        except Exception as msg:
            dbgPrint(msg)
            read_ret = "closing"
            
        if read_ret == "process":
            self.process(fd)
        elif read_ret == "readcontent":
            pass
        elif read_ret == "readmore":
            pass
        elif read_ret == "retry":
            pass
        elif read_ret == "closing":
            self.conn_state[fd].state = "closing"
            self.state_machine(fd)
        else:
            raise Exception("impossible state returned by self.read")
        
    def write2read(self, fd):
        try:
            write_ret = self.write(fd)
        except socket.error, msg:
            write_ret = "closing"
            
        if write_ret == "writemore":
            pass
        elif write_ret == "writecomplete":
            sock_state = self.conn_state[fd]
            conn = sock_state.sock_obj
            self.setFd(conn)
            self.conn_state[fd].state = "read"
            self.epoll_sock.modify(fd, select.EPOLLIN)
        elif write_ret == "closing":
            dbgPrint(msg)
            self.conn_state[fd].state = "closing"
            self.state_machine(fd)
            
            
if __name__ == '__main__':
    def logic(d_in):
        return d_in[::-1]
    
    serverD = nbNet('0.0.0.0', 9076, logic)
    serverD.run()
    