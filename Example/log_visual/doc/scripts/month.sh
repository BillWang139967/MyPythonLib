#########################################################################
# File Name: month.sh
# Author: Bill
# mail: XXXXXXX@qq.com
# Created Time: 2016-08-26 12:13:52
#########################################################################
#!/bin/bash
datebeg=$1
dateend=$2
#read datebeg
#read dateend
beg_s=`date -d "$datebeg" +%s`
end_s=`date -d "$dateend" +%s`
while [ "$beg_s" -lt "$end_s" ]
do
    DATE_ONE=`date -d @$beg_s +"%Y-%m-%d"`
    echo ${DATE_ONE}
    beg_s=$((beg_s+86400))
done
