#-*- coding:utf-8 -*-
import socket
import select
import time

from NetUtils import dbgPrint

__all__ = ["nbNet", "sendData_mh"]

#DEBUG = True
from NetUtils import *

# epoll为I/O多路复用技术
# 多路复用技术select模型、poll模型、epoll模型
# select 模型:1.连接数受限，2.查找匹对速度慢，3.数据由内核拷贝到用户态
# epoll模型:只管'活跃'的连接
#{{{nbNetBase
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
        '''运行程序
        监听epoll是否有新连接过来
        '''
        while True:
            #dbgPrint("\n -- run func loop")
            #for i in self.conn_state.iterkeys():
            #    dbgPrint("\n -- state of fd: %d" % i)
            #    self.conn_state[i].printState();
                
            # epoll对象
            # 最近一次查询后是否有新的需要注册的事件到来，然后根据状态进行执行
            # 如果没有对象到来，epoll就会阻塞在这里
            # epoll是同步IO
            epoll_list = self.epoll_sock.poll()
            for fd, events in epoll_list:
                dbgPrint("\n-- run epoll return fd: %d, event: %s" %(fd, events))
                sock_state = self.conn_state[fd]
                # 确认 epoll状态
                # 如果有io事件，epoll hang住则关闭连接
                if select.EPOLLHUP & events:
                    dbgPrint("events EPOLLHUP")
                    sock_state.state = "closing"
                # 如果IO时间epoll发生错误也关闭连接
                elif select.EPOLLERR & events:
                    dbgPrint("EPOLLERROR")
                    sock_state.state = "closing"
                    
                self.state_machine(fd)

    def state_machine(self, fd):
        """根据状态机状态执行不同方法
        sm 是一个python下的switch使用字典
        如{'x':func0,"y":func1},使用不同的key执行不同的函数
        """
        dbgPrint("\n-- state machine: fd %d, statue is: %s" %(fd, self.conn_state[fd].state))
        # 取出fd状态字典
        sock_state = self.conn_state[fd]
        # 根据fd不同状态执行不同方法
        self.sm[sock_state.state](fd)
#}}}
#{{{nbNet   
class nbNet(nbNetBase):
    def __init__(self, addr, port, logic):
        dbgPrint("\n-- __init__: start!")
        # 链接状态字典，每个链接根据socket链接符建立一个字典，字典中链接状态机
        self.conn_state = {}

        # 1.创建套接字
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        # 2.设置socket选项
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 3.绑定到一个端口
        self.listen_sock.bind((addr, port))
        # 4.侦听连接
        self.listen_sock.listen(10)

        # 使用setFD将根据每个socket链接符存入状态机中
        self.setFd(self.listen_sock)

        # 新建epoll事件对象，后续要监控的事件加入到其中
        self.epoll_sock = select.epoll()
        # 第一个参数向epoll句柄中注册监听socket的可读事件(这个fd用于监听)
        # 第二个使用的是epoll的事件掩码 ，EPOLLIN默认是只读
        self.epoll_sock.register(self.listen_sock.fileno(), select.EPOLLIN)


        # 处理绑定方法
        self.logic = logic
        # 通过不同的状态调用不同的方法
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
        # 如果获取到了socket对象，进行epoll注册，创建状态机
        # 并改变状态机状态为read
        conn = self.accept(fd)
        self.epoll_sock.register(conn.fileno(), select.EPOLLIN)
        self.setFd(conn)
        self.conn_state[conn.fileno()].state = "read"
        
    def read2process(self, fd):
        # 处理read状态，并传入process进行执行
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
#}}}            
            
if __name__ == '__main__':
    def logic(d_in):
        return d_in[::-1]
    
    serverD = nbNet('0.0.0.0', 9076, logic)
    serverD.run()
    
