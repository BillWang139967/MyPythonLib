import traceback

print '########################################################'
print "1/0 Exception Info"
print '---------------------------------------------------------'
try:
    1/0
except Exception, e:
    print '_____________________________________________________'
    print 'str(Exception):\t', str(Exception)
    print 
    print '_____________________________________________________'
    print 'str(e):\t\t', str(e)
    print 
    print '_____________________________________________________'
    print 'repr(e):\t', repr(e)
    print 
    print '_____________________________________________________'
    print 'e.message:\t', e.message
    print 
    print '_____________________________________________________'
    print 'traceback.print_exc():'; traceback.print_exc()
    print 
    print '_____________________________________________________'
    print 'traceback.format_exc():\n%s' % traceback.format_exc()
print '########################################################'
