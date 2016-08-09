def hello(str_info):
    print "hello",str_info

if __name__ == '__main__':
    import sys
    import inspect

    if len(sys.argv) < 2:
        print "Usage:"
        for k, v in globals().items():
            if inspect.isfunction(v) and k[0] != "_":
                print sys.argv[0], k, str(v.func_code.co_varnames[:v.func_code.co_argcount])[1:-1].replace(",", "")
        sys.exit(-1)
    else:
        func = eval(sys.argv[1])
        args = sys.argv[2:]
        func(*args)
