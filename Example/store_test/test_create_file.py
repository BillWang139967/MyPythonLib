#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2017-03-07 22:59:17

# File Name: test_create_file.py
# Description:

"""
import os
import random
import hashlib
import threading
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('./config.ini')

DIR_PATH_NUM= int(config.get('default', 'DIR_PATH_NUM'))
FILE_NUM = int(config.get('default','FILE_NUM'))
PATH_STORE = config.get('default','PATH_STORE')
PATH_LOG_RECORD = config.get('default','PATH_LOG_RECORD')
MAX_FIlE_SIZE_MB = int(config.get('default','MAX_FIlE_SIZE_MB'))

def log(path, data, suffix="log"):
    fout = open(path + "md5log." + suffix, "a")
    fout.write(data)
    fout.write("\n")

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


def write_file(path_store, file_index, dir_index):
    
    ceshi_path = path_store + "/" + dir_index + "/"
    if not os.path.exists(ceshi_path):
        os.makedirs(os.path.dirname(ceshi_path))

    ceshi_full_path = ceshi_path + file_index
    
    
    data = (str(8).zfill(8)) * random.randint(0, 128 * 1024 * MAX_FIlE_SIZE_MB)
    
    fout = open(ceshi_full_path, "w")
    fout.write(data)
    fout.flush()
    md5_ceshifile = get_md5(ceshi_full_path)
    os.rename(os.path.join(ceshi_path, file_index), os.path.join(ceshi_path,md5_ceshifile))
    
    log_data = md5_ceshifile
    log(PATH_LOG_RECORD, log_data, dir_index)
    print dir_index, file_index, log_data
    

def write_files(path_store, file_num, dir_index):
    
    for i in xrange(0, file_num):
        write_file(path_store, str(i), dir_index)
        
def writ_files_mutilthread(path_store, file_num):

    if not os.path.exists(PATH_LOG_RECORD):
        os.makedirs(os.path.dirname(PATH_LOG_RECORD))
    
    threads = []
    
    for i in xrange(0, DIR_PATH_NUM):
        dir_index = str(i);
        t = threading.Thread(target=write_files, args=(path_store, file_num, dir_index))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
        
if __name__ == '__main__':
    writ_files_mutilthread(PATH_STORE, FILE_NUM)
