def hello(str_info, test="world"):
    """
    Args:
        str_info: string
        test: string,defaults:'world'
    """
    print "hello %s -- %s" % (test, str_info)


class CheckCeshiClass():
    @classmethod
    def ceshi_func1(cls, str_info, test="world"):
        """ test classmethod
        Args:
            str_info: string
            test: string,defaults:'world'
        """
        print "hello %s -- %s" % (test, str_info)

    @staticmethod
    def ceshi_func2(str_info):
        """ test staticmethod
        Args:
            str_info: string
        """
        print "hello", str_info


if __name__ == '__main__':
    import sys
    import inspect
    import time
    import os
    root_path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(root_path)

    def _usage(class_name=None):
        print "Usage:"
        prefix = "Check"
        if class_name is None:
            for k, v in sorted(globals().items(), key=lambda item: item[0]):
                if inspect.isfunction(v) and k[0] != "_":
                    args, __, __, defaults = inspect.getargspec(v)
                    if defaults:
                        print sys.argv[0], k, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                            str(["%s=%s" % (a, b) for a, b in zip(
                                args[-len(defaults):], defaults)])[1:-1].replace(",", "")
                    else:
                        print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[
                            1:-1].replace(",", "")
                if inspect.isclass(v) and k.startswith(prefix):
                    print sys.argv[0], k
            sys.exit(-1)
        if class_name not in globals():
            print "not found class_name[%s]" % class_name
            sys.exit(-1)
        for class_k, class_v in sorted(
                globals()[class_name].__dict__.items(), key=lambda item: item[0]):
            if str(class_v)[0] == "_":
                continue
            if str(class_v).startswith("<staticmethod") or str(
                    class_v).startswith("<classmethod"):
                class_func_str = "%s.%s" % (class_name, class_k)
                class_func = eval(class_func_str)
                args, __, __, defaults = inspect.getargspec(class_func)
                if "cls" in args:
                    args.remove("cls")
                # class_func.func_code.co_varnames[:class_func.func_code.co_argcount] is tuple
                class_func_args=list(class_func.func_code.co_varnames[:class_func.func_code.co_argcount])
                if "cls" in class_func_args:
                    class_func_args.remove("cls")
                if defaults:
                    print sys.argv[0], class_func_str, str(args[:-len(defaults)])[1:-1].replace(",", ""), \
                        str(["%s=%s" % (a, b) for a, b in zip(
                            args[-len(defaults):], defaults)])[1:-1].replace(",", "")
                else:
                    print sys.argv[0], class_func_str, str(class_func_args)[1:-1].replace(",", "")
        sys.exit(-1)
    if len(sys.argv) < 2:
        _usage()
    else:
        func_name = sys.argv[1]
        if func_name in globals() and inspect.isclass(globals()[func_name]):
            _usage(func_name)
        try:
            func = eval(func_name)
        except NameError:
            _usage()
        args = sys.argv[2:]
        now_start = int(time.time())
        timeArray = time.localtime(now_start)
        timeStr = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print "\x1B[;36m[start time]\x1B[0m:%s" % timeStr
        try:
            r = func(*args)
        except Exception as e:
            print "Usage:"
            print "\t", "python %s" % sys.argv[1], str(
                func.func_code.co_varnames[:func.func_code.co_argcount])[1:-1].replace(",", "")
            if func.func_doc:
                print "\n".join(["\t\t" + line.strip()
                                 for line in func.func_doc.strip().split("\n")])
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
        print "\x1B[;36m[consum time]\x1B[0m %s m:%s s" % (
            time_consum_minute, time_consum_second)
        if isinstance(r, int):
            sys.exit(r)
