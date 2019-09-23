# -*- coding:utf-8 -*-
import sys
import os
import time
import atexit
from signal import SIGTERM


class Daemon(object):
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method

    编写守护进程的一般步骤步骤：
    （1）创建自己成并被 init 进程接管：在父进程中执行 fork 并 exit 退出；
    （2）创建新进程组和新会话：在子进程中调用 setsid 函数创建新的会话；
    （3）修改子进程的工作目录：在子进程中调用 chdir 函数，让根目录 "/" 成为子进程的工作目录；
    （4）修改子进程 umask：在子进程中调用 umask 函数，设置进程的 umask 为 0；
    （5）在子进程中关闭任何不需要的文件描述符

    在子进程中再次 fork 一个进程，这个进程称为孙子进程，之后子进程退出
    重定向孙子进程的标准输入流、标准输出流、标准错误流到 /dev/null
    那么最终的孙子进程就称为守护进程。
    """

    def __init__(self,
                 pidfile='./run/daemon.pid',
                 stdin='/dev/null',
                 stdout='./log/stdout.log',
                 stderr='./log/stderr.log'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(
                "fork #1 failed: %d (%s)\n" %
                (e.errno, e.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        # 创建新会话，子进程成为新会话的首进程（session leader）
        '''
        setsid()函数可以建立一个对话期。

        会话期(session)是一个或多个进程组的集合。
        如果，调用 setsid 的进程不是一个进程组的组长，此函数创建一个新的会话期。
        (1)此进程变成该对话期的首进程
        (2)此进程变成一个新进程组的组长进程。
        (3)此进程没有控制终端，如果在调用setsid前，该进程有控制终端，那么与该终端的联系被解除。 如果该进程是一个进程组的组长，此函数返回错误。
        (4)为了保证这一点，我们先调用fork()然后exit()，此时只有子进程在运行
        '''
        # 创建新的会话，子进程成为会话的首进程
        # 控制终端，登录会话和进程组通常是从父进程继承下来的。我们的目的就是要摆脱它们，使之不受它们的影响。方法是在创建子进程的基础上，调用setsid()使进程成为会话组长
        os.setsid()

        '''
        由于umask会屏蔽权限，所以设定为0，这样可以避免读写文件时碰到权限问题。
        '''
        os.umask(0)

        '''
        现在，进程已经成为无终端的会话组长。但它可以重新申请打开一个控制终端。可以通过使进程不再成为会话组长来禁止进程重新打开控制终端：
        '''
        # do second fork
        try:
            # 创建孙子进程，而后子进程退出
            # 新创建的孙子进程，不是会话组长
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(
                "fork #2 failed: %d (%s)\n" %
                (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        # os.dup2(fd, fd2); 后将 fd 代表的那个文件（可以想象成是P_fd指针）强行复制给 fd2
        # 也就是重定向，将标准输入，标准输出，标准错误重定向到指定文件中
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while True:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """

    def get_pid(self):
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid

    def is_running(self):
        pid = self.get_pid()
        # print(pid)
        return pid and os.path.exists('/proc/%d' % pid)


if __name__ == "__main__":
    def helloworld():
        import time
        # stdout 文件默认开启的缓冲写，所以需要隔一段时间才能看到日志中有文件写入
        # open 函数中有一个 bufferin 的参数，默认是 -1，如果设置为 0 时，就是无缓冲模式
        # open("./log/test.txt",'a+',buffering=0)
        while True:
            print "helloworld"
            print "Start : %s" % time.ctime()
            time.sleep(1)
            print "End : %s" % time.ctime()

    class MyDaemon(Daemon):
        def run(self):
            helloworld()
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
