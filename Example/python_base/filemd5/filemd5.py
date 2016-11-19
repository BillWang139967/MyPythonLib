#!/usr/bin/python
try:
    import hashlib,sys
except Exception,e:
    print e
    sys.exit(1)

def main(filename):
    m = hashlib.md5()
    fp=open(filename, 'rb')
    while True:
        blk = fp.read(4096) # 4KB per block
        if not blk: break
        m.update(blk)
    return  m.hexdigest()

def md5new(filename):
    return hashlib.md5(open(filename).read()).hexdigest()

if __name__ == '__main__':
    try:
        print main(sys.argv[1])
        print md5new(sys.argv[1])
    except:
        sys.exit('Usage: %s file' % sys.argv[0])
