#!/usr/bin/env python 

import sys
import getopt

def Usage():
    print 'PyTest.py usage:'
    print '-h,--help: print help message.'
    print '-v, --version: print script version'
    print '-o, --output: input an output verb'
    print '--foo: Test option '
    print '--fre: another test option'
def Version():
    print 'PyTest.py 1.0.1'
def OutPut(args):
    print 'Hello, %s'%args
def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hvo:', ['output=', 'foo=', 'fre='])
        # opts [('-o', 'wang')]
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif o in ('-o', '--output'):
            OutPut(a)
            sys.exit(0)
        elif o in ('--foo',):
            Foo=a
        elif o in ('--fre',):
            Fre=a
        else:
            print 'unhandled option'
            sys.exit(3)

if __name__ == '__main__':
    main(sys.argv)
