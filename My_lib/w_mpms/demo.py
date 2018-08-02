# coding=utf-8
"""
Do parallel python works easily in multithreads in multiprocesses
一个简单的多进程-多线程工作框架

工作模型:
    主线程不断向队列中添加任务参数
    外部进程的大量线程(工作函数)不断从任务队列中读取参数,并行执行后将结果加入到结果队列
    主线程中新开一个处理线程,不断从结果队列读取并依此处理

Due to many threads, some time-consuming tasks would finish much faster than single threads
可以显著提升某些长时间等待的工作的效率,如网络访问
"""
from __future__ import unicode_literals, print_function
from time import time, sleep

import w_lib.mpms

def _worker(index, t=None):
    """
    Worker function, accept task parameters and do actual work
    should be able to accept at least one arg
    ALWAYS works in external thread in external process

    工作函数,接受任务参数,并进行实际的工作
    总是工作在外部进程的线程中 (即不工作在主进程中)
    """
    sleep(0.2)  # delay 0.2 second
    #print(index, t)

    # worker's return value will be added to product queue, waiting handler to handle
    # you can return any type here (Included the None , of course)
    # worker函数的返回值会被加入到队列中,供handler依次处理,返回值允许除了 StopIteration 以外的任何类型
    return index, "hello world"
def main():
    results = ""
    # we will run the benchmarks several times using the following params
    # 下面这些值用于多次运行,看时间
        # Init the poll  # 初始化
    m = w_lib.mpms.MPMS(_worker,processes=1,threads=10)
    m.start()  # start and fork subprocess
    start_time = time()  # when we started  # 记录开始时间

    # put task parameters into the task queue, 2000 total tasks
    # 把任务加入任务队列,一共2000次
    for i in range(200):
        m.put(i, t=time())

    # close task queue and wait all workers and handler to finish
    # 等待全部任务及全部结果处理完成
    m.join()
    print(m.get_result())

    # write and print records
    # 下面只是记录和打印结果
    results +=  " TotalTime: " + str(time() - start_time)
    print(results)

if __name__ == '__main__':
    import sys, inspect
    if len(sys.argv) < 2:
        print("Usage:")
        for k, v in sorted(globals().items(), key=lambda item: item[0]):
            if inspect.isfunction(v) and k[0] != "_":
                args, __, __, defaults = inspect.getargspec(v)
                if defaults:
                    print(sys.argv[0], k, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                          str(["%s=%s" % (a, b) for a, b in zip(args[-len(defaults):], defaults)])[1:-1].replace(",", ""))
                else:
                    print(sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[1:-1].replace(",", ""))
        sys.exit(-1)
    else:
        func = eval(sys.argv[1])
        args = sys.argv[2:]
        try:
            r = func(*args)
        except Exception, e:
            print("Usage:")
            print("\t", "python %s" % sys.argv[1], str(func.func_code.co_varnames[:func.func_code.co_argcount])[1:-1].replace(",", ""))
            if func.func_doc:
                print("\n".join(["\t\t" + line.strip() for line in func.func_doc.strip().split("\n")]))
            print(e)
            r = -1
            import traceback
            traceback.print_exc()
        if isinstance(r, int):
            sys.exit(r)
