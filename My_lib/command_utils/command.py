def hello(str_info):
    """
    str_info: string
    """
    print "hello",str_info

if __name__ == '__main__':
    import sys, inspect
    import time
    if len(sys.argv) < 2:
        print "Usage:"
        for k, v in sorted(globals().items(), key=lambda item: item[0]):
            if inspect.isfunction(v) and k[0] != "_":
                args, __, __, defaults = inspect.getargspec(v)
                if defaults:
                    print sys.argv[0], k, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                          str(["%s=%s" % (a, b) for a, b in zip(args[-len(defaults):], defaults)])[1:-1].replace(",", "")
                else:
                    print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[1:-1].replace(",", "")
        sys.exit(-1)
    else:
        try:
            func = eval(sys.argv[1])
        except NameError:
            print "Usage:"
            for k, v in sorted(globals().items(), key=lambda item: item[0]):
                if inspect.isfunction(v) and k[0] != "_":
                    args, __, __, defaults = inspect.getargspec(v)
                    if defaults:
                        print sys.argv[0], k, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                              str(["%s=%s" % (a, b) for a, b in zip(args[-len(defaults):], defaults)])[1:-1].replace(",", "")
                    else:
                        print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[1:-1].replace(",", "")
            sys.exit(-1)
        args = sys.argv[2:]
        now_start = int(time.time())
        timeArray = time.localtime(now_start)
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print "\x1B[;36m[start time]\x1B[0m:%s" % timeStr
        try:
            r = func(*args)
        except Exception, e:
            print "Usage:"
            print "\t", "python %s" % sys.argv[1], str(func.func_code.co_varnames[:func.func_code.co_argcount])[1:-1].replace(",", "")
            if func.func_doc:
                print "\n".join(["\t\t" + line.strip() for line in func.func_doc.strip().split("\n")])
            print e
            r = -1
            import traceback
            traceback.print_exc()
        now_end = int(time.time())
        timeArray = time.localtime(now_end)
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print "\x1B[;36m[end time]\x1B[0m :%s" % timeStr
        time_consum = now_end - now_start
        time_consum_minute = time_consum / 60
        time_consum_second = time_consum % 60
        print "\x1B[;36m[consum time]\x1B[0m %s m:%s s" % (time_consum_minute,time_consum_second)
        if isinstance(r, int):
            sys.exit(r)

