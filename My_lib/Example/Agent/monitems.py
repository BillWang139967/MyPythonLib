#!/usr/bin/env python
#-*- coding:utf-8 -*-
import inspect
import os, socket, time

class Mon:
    def __init__(self):
        self.data = {}

    def getLoadAvg(self):
        with open("/proc/loadavg") as f:
            a = f.read().split()[:3]
            return float(a[0])

    def getMemTotal(self):
        with open("/proc/meminfo") as f:
            a = int(f.readline().split()[1])
            return a/1024

    def getMemUsage(self, noBufferCache=True):
        if noBufferCache:
            with open("/proc/meminfo") as f:
                T = int(f.readline().split()[1])
                F = int(f.readline().split()[1])
                B = int(f.readline().split()[1])
                C = int(f.readline().split()[1])
                return (T-F-B-C)/1024
        else:
            with open("/proc/meminfo") as f:
                a = int(f.readline().split()[1]) - int(f.readline().split()[1])
                return a/1024
    
    def getMemFree(self, noBufferCache=True):
        if noBufferCache:
            with open("/proc/meminfo") as f:
                T = int(f.readline().split()[1])
                F = int(f.readline().split()[1])
                B = int(f.readline().split()[1])
                C = int(f.readline().split()[1])
                return (F+B+C)/1024
        else:
            with open("/proc/meminfo") as f:
                f.readline()
                a = int(f.readline().split()[1])
                return a/1024

    def getHost(self):
        return socket.gethostname()

    def getTime(self):
        return int(time.time())

    def runAllGet(self):
        for fun in inspect.getmembers(self, predicate=inspect.ismethod):
            if fun[0][:3] == "get":
                self.data[fun[0][3:]] = fun[1]()
        return self.data

if __name__ == "__main__":
    print Mon().runAllGet()
    print Mon().getMemTotal()

