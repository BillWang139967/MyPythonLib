# date

## 批量输出一段日期内的每一天

```
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
```
下载

```
#curl -o month.sh "https://raw.githubusercontent.com/BillWang139967/python_learn/master/log_visual/doc/scripts/month.sh"
#sh month.sh 20160701 20160801
```
