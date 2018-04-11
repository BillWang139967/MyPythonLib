#!/usr/bin/python
#coding=utf8
"""
# Author: meetbill
# Created Time : 2016-09-05 19:57:09

# File Name: file_util.py
# Description:
# Package for  operations.
"""

import sys
import re

reload(sys)  
sys.setdefaultencoding('utf8')

# 需要修改，配置文件位置

def _loadconfig(cfgfile=None, detail=False):
    """Read config file and parse config item to dict.
    """
    settings = {}
    with open(cfgfile) as f:
        for line_i, line in enumerate(f):
            # line_i[行号]，line[每行内容]
            
            # 删除空白符(包括'\n', '\r',  '\t',  ' ')
            line = line.strip()
            
            # 跳过空行和注释('# '开头的)
            if not line or line.startswith('# '): continue
            
            # detect if it's commented
            if line.startswith('#'):
                line = line.strip('#')
                commented = True
                if not detail: continue
            else:
                commented = False
            # 将行以第一个'='分割
            #########################################
            fs = re.split('=', line, 1)
            if len(fs) != 2: continue

            item = fs[0].strip()
            value = fs[1].strip()

            if settings.has_key(item):
                if detail: count = settings[item]['count']+1
                if not commented:
                    settings[item] = detail and {
                        'file': cfgfile,
                        'line': line_i,
                        'value': value,
                        'commented': commented,
                    } or value
            else:
                count = 1
                settings[item] = detail and {
                    'file': cfgfile,
                    'line': line_i,
                    'value': fs[1].strip(),
                    'commented': commented,
                } or value
            if detail: settings[item]['count'] = count
            
    return settings
def cfg_get(config_file,item,detail=False):
    """
    功能:获取配置文件中某个 item 的值

    config_file:配置文件位置
    item:获取项
    detail:详细显示，显示 item 在多少行以及是否为注释状态等等
    
    例子:python file_util.py cfg_get ./config s3_addr
    """
    config = _loadconfig(config_file,detail=detail)
    if config.has_key(item):
        print config[item]
        return config[item]
    else:
        return None
def cfg_set(config_file,item, value, commented=False):
    """
    功能:对某配置进行修改，如果可以获取到 key，则对 key 后的 item 进行修改如果获取不到 key，则直接在配置文件后进行追加一行

    config_file:配置文件位置
    item:获取项
    value:某项要更改的值
    commented:配置的时候是否配置为注释状态
    
    例子:python file_util.py cfg_set ./config s3_addr 192.168.1.3
    """
    v = cfg_get(config_file,item, detail=True)
    #print v

    if v:
        # detect if value change
        if v['commented'] == commented and v['value'] == value: return True
        
        # empty value should be commented
        # 如果有key，但是传的value值为空，会将此行进行注释
        if value == '': commented = True

        # replace item in line
        lines = []
        with open(v['file']) as f:
            for line_i, line in enumerate(f):
                if line_i == v['line']:
                    # 对没注释的行进行操作
                    if not v['commented']:
                        # 检测是否需要注释
                        if commented:
                            if v['count'] > 1:
                                # delete this line, just ignore it
                                pass
                            else:
                                # comment this line
                                #########################################
                                lines.append('#%s=%s\n' % (item, value))
                        else:
                            #########################################
                            lines.append('%s=%s\n' % (item, value))
                    else:
                        if commented:
                            # do not allow change comment value
                            lines.append(line)
                            pass
                        else:
                            # append a new line after comment line
                            lines.append(line)
                            #########################################
                            lines.append('%s=%s\n' % (item, value))
                else:
                    lines.append(line)
        with open(v['file'], 'w') as f: f.write(''.join(lines))
    else:
        # append to the end of file
        with open(config_file, 'a') as f:
            #########################################
            f.write('\n%s%s = %s\n' % (commented and '#' or '', item, value))
    print "new"
    cfg_get(config_file,item, detail=True)
    return True



if __name__ == '__main__':
    import sys, inspect                                                                                                                                                                        
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
        func = eval(sys.argv[1])
        args = sys.argv[2:]
        try:
            r = func(*args)
        except Exception, e:
            print "Usage:"
            print "\t", "python %s %s" % (sys.argv[0],sys.argv[1]),str(func.func_code.co_varnames[:func.func_code.co_argcount])[1:-1].replace(",", "") 
            if func.func_doc:
                print "\n".join(["\t\t" + line.strip() for line in func.func_doc.strip().split("\n")])
            print e
            r = -1
            import traceback
            traceback.print_exc()
        if isinstance(r, int):
            sys.exit(r)
