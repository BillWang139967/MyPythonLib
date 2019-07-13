#!/usr/bin/python
# coding=utf8
"""
# Author: meetbill
# Created Time : 2019-07-13 12:38:31

# File Name: py_count.py
# Description:

#统计代码量，显示离10W行代码还有多远
#递归搜索各个文件夹
#显示各个类型的源文件和源代码数量
#显示总行数与百分比

"""

import os
import io

file_list={}
source_list={}
#查找文件
def _find_file(file_path,target):
    os.chdir(file_path)
    all_files=os.listdir(os.curdir)
    for each in all_files:
        fext=os.path.splitext(each)[1]
        # fext 是文件后缀，比如 .py
        if fext in target:
            lines=_calc_code(each) #统计行数
            # print("文件%s的代码行数是%d"%(each,lines))
            #统计文件数
            try:
                file_list[fext]+=1
            except KeyError:
                file_list[fext]=1
            #统计源代码行数
            try:
                source_list[fext] += lines
                #print(source_list[fext])
            except KeyError:
                source_list[fext] = lines
                #print(source_list[fext])
        if os.path.isdir(each):
            _find_file(each,target) # 递归调用
            os.chdir(os.pardir) #返回上层目录


#统计行数
def _calc_code(file_name):
    pwd = os.getcwd()
    with io.open(file_name,'r',encoding='utf-8') as f:
        # print("正在分析文件%s..."%file_name)
        try:
        #    for eachline in f:
        #        lines += 1
            code_lines = 0          # 代码行数
            comment_lines = 0       # 注释行数
            blank_lines = 0         # 空白行数  内容为'\n',strip()后为''
            is_comment = False
            start_comment_index = 0 # 记录以'''或"""开头的注释位置
            tota_lines = 0          # 总行数
            for index,line in enumerate(f,start=1):
                tota_lines += 1
                line = line.strip() #去除开头和结尾的空白符
                # 判断多行注释是否已经开始
                if not is_comment:
                    if line.startswith("'''") or line.startswith('"""'):
                        is_comment = True
                        start_comment_index = index
                    #单行注释
                    elif line.startswith('#'):
                        comment_lines += 1
                    #空白行
                    elif line == '':
                        blank_lines += 1
                    #代码行
                    else:
                        code_lines += 1
                #多行注释已经开始
                else:
                    if line.endswith("'''") or line.endswith('"""'):
                        is_comment = False
                        comment_lines += index - start_comment_index + 1
                    else:
                        pass

        except UnicodeDecodeError:
            pass
        assert tota_lines == code_lines + blank_lines + comment_lines
        print("文件 %s/%s 分析完毕，包含[代码行]:%d [空行]:%d [注释行]:%d [总行]:%d" %(pwd,file_name,code_lines,blank_lines,comment_lines,tota_lines))
    return code_lines


#显示结果
def _show_result(start_dir):
    lines=0
    total=0
    text=''

    for i in source_list:
        lines=source_list[i]
        total+=lines
        text+='%s源文件%d个，源代码%d行\n'%(i,file_list[i],lines )

    title='统计结果'
    msg='目前代码行数：%d\n完成进度：%.2f%%\n距离十万行代码还差%d行'%(total,total/1000,100000-total)
    print "%s|%s|%s" % (msg,title,text)

def count(path):
    if not os.path.isdir(path):
        print "%s is not dir" % path
        sys.exit(-1)
    target=['.py','.java','.c','.cc','.cpp']  #定义需要查找的源文件类型
    _find_file(path,target)
    print "##########################################"
    _show_result(path)

if __name__ == "__main__":
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
            print "\t", "python %s" % sys.argv[1], str(func.func_code.co_varnames[:func.func_code.co_argcount])[1:-1].replace(",", "")
            if func.func_doc:
                print "\n".join(["\t\t" + line.strip() for line in func.func_doc.strip().split("\n")])
            print e
            r = -1
            import traceback
            traceback.print_exc()
        if isinstance(r, int):
            sys.exit(r)
