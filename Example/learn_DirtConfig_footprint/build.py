#encoding:utf-8
import requests
import os,sys
import config
reload(sys)
sys.setdefaultencoding("utf-8")
import requests
import json
import random
#{{{html
htmlStr = '''

<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <title>%(title)s</title>
</head>
<body>

    <div id="main" style="height:600px;width:900px;margin:20px auto;"></div>
    <script src="http://echarts.baidu.com/build/dist/echarts-all.js"></script>
    <script type="text/javascript">
        var myChart = echarts.init(document.getElementById('main'));
        var option = {
            backgroundColor: '#1b1b1b',
            color: ['gold', 'aqua', 'lime'],
            title: {
                text: '%(title)s',
                subtext: '%(subtitle)s',
                x: 'center',
                textStyle: {
                    color: '#fff'
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: '{b}'
            },
            dataRange: {
                show:false,
                min : 0,
                max : 100,
                calculable : true,
                color: ['#ff3333', 'orange', 'yellow','lime','aqua'],
                textStyle:{
                    color:'#fff'
                }
            },
            series: [{
                name: '全国',
                type: 'map',
                roam: true,
                hoverable: false,
                mapType: '%(region)s',
                itemStyle: {
                    normal: {
                        borderColor: 'rgba(100,149,237,1)',
                        borderWidth: 0.5,
                        areaStyle: {
                            color: '#1b1b1b'
                        }
                    }
                },
                data: [],

                geoCoord: %(alldata)s
            }, {
                name: '足迹',
                type: 'map',
                mapType: '%(region)s',
                data: [],
                markLine: {
                    smooth: true,
                    effect: {
                        show: true,
                        scaleSize: 1,
                        period: 30,
                        color: '#fff',
                        shadowBlur: 10
                    },
                    itemStyle: {
                        normal: {
                            borderWidth: 1,
                            lineStyle: {
                                type: 'solid',
                                shadowBlur: 10
                            },
                            label:{
                                show:false
                            },

                        }
                    },

                    data: %(linedata)s
                },
                markPoint: {
                    symbol: 'emptyCircle',
                    symbolSize: function(v) {
                        return 10 + v / 10
                    },
                    effect: {
                        show: true,
                        shadowBlur: 0
                    },
                    itemStyle: {
                        normal: {
                            label: {
                                show: false
                            }
                        },
                        emphasis: {
                            label: {
                                position: 'top'
                            }
                        }
                    },
                    data: %(pointdata)s
                }
            }]
        };
        myChart.setOption(option);
    </script>
</body>
</html>

'''.replace('\n','')
# .replace('<','&lt;').replace('>','&gt;')

#}}}

class FootPrint():
    # get config
    def __init__(self,config):
        self.key = 'q5mTrTGzCSVq5QmGpI9y18Bo'
        self.url = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak=%s&address=' % (self.key)
        # dirt.get('key',default=None)
        self.title = config.get('title','2015年行程')
        print self.title
        self.color = config.get('color',None)
        self.subtitle = config.get('subtitle')
        print self.subtitle
        self.data = config['foot']
        self.region = config.get('region','china')
        self.alldata = {}
        self.linedata = []
        self.pointdata = []
        self.cache = {}
    def processData(self):
        # self.data is a list
        for route in self.data:
            # route is a spring
            print route
            # spring.split --> list tmp
            tmp = route.split()
            for t in tmp:
				# print t
                # self.cache is a dict
                self.cache[t] = self.getValue()
                if t not in self.alldata:
                    self.getPoint(t)

            for i in range(len(tmp)-1):
                val = self.getValue()
                self.linedata.append([{'name':tmp[i]},{"name":tmp[i+1],'value':self.cache[tmp[i+1]]}])
        for name in self.alldata:
            self.pointdata.append({'name':name,'value':self.cache[name]})

    def getPoint(self,name):
        url = self.url+name
        try:
            r = requests.get(url)
            res = r.json()
            if res.get('result',None):
                loc = res['result']['location']
                self.alldata[name] = [loc['lng'],loc['lat']]
        except:
            print '获取不到%s的经纬度信息'%(name)
    def writeFile(self):
        obj = {
            'title':self.title,
            'subtitle':self.subtitle,
            'region':self.region,
            'alldata':json.dumps(self.alldata),
            'linedata':json.dumps(self.linedata),
            'pointdata':json.dumps(self.pointdata)
        }

        with open('footprint.html','w') as f:
            f.write(htmlStr % obj)
        print '成功生成文件，打开看看吧！'
    def getValue(self):
        if self.color:
            return random.randint(0,100)
        else:
            return 1
    def start(self):
        self.processData()
        self.writeFile()      

if __name__ =="__main__":
    F = FootPrint(config.config)
    F.start()
