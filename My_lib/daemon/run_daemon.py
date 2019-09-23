#!/usr/bin/env python
# coding=utf8
import os
import sys
from xlib import daemon

import ceshi
class MyDaemon(daemon.Daemon):
    def run(self):
        ##########################################需要修改部分
        ceshi.ceshi()
        ##########################################

if __name__ == "__main__":
    ######################################
    # edit this code
    cur_dir = os.getcwd()
    if not os.path.exists("{cur_dir}/run/".format(cur_dir=cur_dir)):
        os.makedirs("./run")

    if not os.path.exists("{cur_dir}/log/".format(cur_dir=cur_dir)):
        os.makedirs("./log")

    my_daemon = MyDaemon(
        pidfile="{cur_dir}/run/daemon.pid".format(cur_dir=cur_dir),
        stdout="{cur_dir}/log/daemon_stdout.log".format(cur_dir=cur_dir),
        stderr="{cur_dir}/log/daemon_stderr.log".format(cur_dir=cur_dir)
    )

    if len(sys.argv) == 3:
        daemon_name = sys.argv[1]
        if 'start' == sys.argv[2]:
            my_daemon.start()
        elif 'stop' == sys.argv[2]:
            my_daemon.stop()
        elif 'restart' == sys.argv[2]:
            my_daemon.restart()
        elif 'status' == sys.argv[2]:
            alive = my_daemon.is_running()
            if alive:
                print('process [%s] is running ......' % my_daemon.get_pid())
            else:
                print('daemon process [%s] stopped' % daemon_name)
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s agent|server start|stop|restart|status" % sys.argv[0]
        sys.exit(2)
