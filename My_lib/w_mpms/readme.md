# w_mpms
<!-- vim-markdown-toc GFM -->

* [1 简介](#1-简介)
* [2 run](#2-run)
    * [version](#version)

<!-- vim-markdown-toc -->

## 1 简介
Simple python Multiprocesses-Multithreads queue
简易 Python 多进程 - 多线程任务队列
（自用，ap 不为生产环境下造成的任何损失和灵异现象负责）

在多个进程的多个线程的 worker 中完成耗时的任务，并在主进程的 collector 中处理结果

支持 python 2.7/3.4+

## 2 run

```python
from w_lib.mpms import MPMS
import random
import time

def worker(i, j=None):
    time.sleep(3)
    return i,j

def main():
    m = MPMS(
        worker,
        processes=1,
        threads=100,  # 每进程的线程数
    )
    m.start()
    for i in range(200):  # 你可以自行控制循环条件
        m.put(i, random.randint(0,99))  # 这里的参数列表就是 worker 接受的参数
    m.join()
    result = m.get_result()
    print result

if __name__ == '__main__':
    main()
```
更多请看 `demo.py`

### version

> * V2.0.0.3
>   * (1) 日志中输出目前任务进度信息
> * V2.0.0.2
>   * (1) 去掉了 collector 函数
>   * (2) 去掉了 Meta 类
> * V2.0.0.1
>   * (1) 增加输出日志到 /tmp/mpms.log
>   * (2) 当进程数为 1 时，使用的队列自动修改为 Queue（当使用的 python 版本没有开启 sem_open 时使用，即无法使用多进程库 multiprocessing)
> * V2.0.0.0
>   * [原程序 mpms](https://github.com/aploium/mpms)
