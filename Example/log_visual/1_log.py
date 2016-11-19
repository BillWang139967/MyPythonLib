# coding=utf-8
import re
f = open('./acc.log')
res = {}
for l in f:
    try:
        arr = re.split(' |\t',l)
        # 获取ip url 和status
        module = arr[3]
        ip = arr[4]
        status = arr[7]
        interface = arr[8]
        # ip url 和status当key，每次统计+1
        res[(module,ip,status,interface)] = res.get((module,ip,status,interface),0)+1
    except:
        pass
# 生成一个临时的list
res_list = [(k[0],k[1],k[2],k[3],v) for k,v in res.items()]
# 按照统计数量排序，打印前10
for k in sorted(res_list,key=lambda x:x[4],reverse=True)[:10]:
    print k
