#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2017-10-19 10:42:21

# File Name: easyrun.py
# Description:

# v1.0.4

"""
import subprocess
import time
import os
import signal


class Result(object):
    def __init__(self, command=None, retcode=None, output=None):
        self.command = command or ''
        self.retcode = retcode
        self.output = output
        self.success = False
        if retcode == 0:
            self.success = True


def run(command):
    process = subprocess.Popen(command, shell=True)
    process.communicate()
    return Result(command=command, retcode=process.returncode)


def run_timeout(command, timeout=10):
    timeout = int(timeout)
    process = subprocess.Popen(
        command,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        shell=True)
    t_beginning = time.time()
    seconds_passed = 0
    while True:
        if process.poll() is not None:
            break
        seconds_passed = time.time() - t_beginning
        if timeout and seconds_passed > timeout:
            process.terminate()
            return Result(command=command, retcode=124, output="timeout")
        time.sleep(0.1)
    output, _ = process.communicate()
    return Result(command=command, retcode=process.returncode, output=output)


def run_capture(command):
    outpipe = subprocess.PIPE
    errpipe = subprocess.STDOUT
    process = subprocess.Popen(command, shell=True, stdout=outpipe,
                               stderr=errpipe)
    output, _ = process.communicate()
    output = output.strip('\n')
    return Result(command=command, retcode=process.returncode, output=output)


def run_capture_limited(command, maxlines=20000):

    import collections
    import threading

    lines = collections.deque(maxlen=maxlines)

    def reader_thread(stream, lock):
        for line in stream:
            lines.append(line)
    outpipe = subprocess.PIPE
    errpipe = subprocess.STDOUT
    process = subprocess.Popen(command, shell=True, stdout=outpipe,
                               stderr=errpipe)
    lock = threading.Lock()
    thread = threading.Thread(
        target=reader_thread, args=(
            process.stdout, lock))
    thread.start()

    process.wait()
    thread.join()

    return Result(command=command, retcode=process.returncode,
                  output=''.join(lines))


def run_killpid(pid):
    os.kill(pid, signal.SIGTERM)


if __name__ == '__main__':
    print('---[ .success ]---')
    print(run('ls').success)
    print(run('dir').success)

    print('---[ .retcode ]---')
    print(run('ls').retcode)
    print(run('dir').retcode)

    print('---[ capture ]---')
    print(len(run_capture('ls').output))

    print('---[ limited capture ]---')
    print(run_capture_limited('ls', maxlines=2).output)

    print('---[ timeout ]---')
    print(run_timeout('curl -s www.baidu.com', timeout=3).output)
