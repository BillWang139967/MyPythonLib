#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2017-03-07 22:56:46

# File Name: test_check.py
# Description:

"""

import os
import threading
import hashlib
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('./config.ini')
PATH_STORE = config.get('default','PATH_STORE')
LOG_PATH = config.get('default','PATH_LOG_RECORD')
DIR_PATH_NUM= int(config.get('default', 'DIR_PATH_NUM'))


def logfail(data):

    if not os.path.exists(LOG_PATH):
        os.makedirs(os.path.dirname(LOG_PATH))

    path = LOG_PATH + "failed.log"

    fout = open(path, "a")
    fout.write(data + "\n")  # it's thread-safe
    fout.flush()
    
def get_md5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()
    
def check_file(path, file_name):
    full_file_name = path + file_name
    md5 = get_md5(full_file_name)
    if md5 != file_name:
        logfail(full_file_name)
        print "Check failed:", md5
    else:
        print "Check pass"

def ckeck_file_list(file_path):
    file_list = os.listdir(file_path)
    for file_name in file_list:
        if not str(file_name).startswith("."):
            check_file(file_path, file_name)

def check_files_mutilthread(path_store, dir_num):
    threads = []
    
    for i in xrange(0, dir_num):
        dir_index = str(i);
        file_path = path_store + "/" + dir_index + "/"
        t = threading.Thread(target=ckeck_file_list, args=(file_path,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

if __name__ == '__main__':
    check_files_mutilthread(PATH_STORE, DIR_PATH_NUM)
