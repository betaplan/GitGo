import urllib
import requests
import pandas as pd
import re
import time
import json
import datetime as dt
from tushare.stock import cons as ct
from datetime import datetime
import os
import requests
import io
from pandas import Series
import urllib.request
import json
import csv
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
import random
import sys
sys.path.append('/easyquotation.easyquotation')
sys.path.append(r'C:\Users\ln_ti\PycharmProjects\GitGo\cn_stock_163')

codebook = { "0": "sz",
             "6": "sh",
             "3": "sz",
             }

eastcode = { "0": "0",
             "6": "1",
             "3": "0",
             }

mapping = {
"f57":"代码",
"f58":"公司名",
"f116":"总市值",
"f117":"流通市值",
"f167":"市净率",
"f162":"动态市盈率",
"f163":"静态市盈率",
"f164":"滚动市盈率",
"f47":"成交量",
"f48":"成交额",
"f46":"今开",
"f60":"昨收",
"f127":"行业板块",
"f128":"地区板块",
"f129":"其他板块",
"f168":"换手",
"f44":"最高",
"f45":"最低",
}

dirlocation = os.path.dirname(os.path.abspath(__file__))

cur_folder = dirlocation +'\\eastmoney\\'

'''
f57	f58	f116	f117	f167	f162	f163	f164	f47	f48	f46	f60	f127	f128	f129	f168	f44	f45
代码	公司名	总市值	流通市值	市净率	动态市盈率	静态市盈率	滚动市盈率	成交量	成交额	今开	昨收	行业板块	地区板块	其他板块	换手	最高	最低

'''
def get_json(url):  # 获取JSON
    try:
        r = requests.get(url)  # 抓取网页返回json信息
        r.encoding = 'utf-8'
        # print(r.json())
        # with open(r"C:\Users\xxp\.spyder-py3\testcode\tmp.txt", "w") as fp:
        # fp.write(json.dumps(r.json(),indent=4,ensure_ascii=False)) # txt测试是否成功获取网页
        return r.json()
    except:
        return 'false'


def Get_stock_Background(code = '000001'):

    _querynumber = random.randrange(1000000000)
    _code = codebook.get(code[:1])
    _eastcode = eastcode.get(code[:1])
    url = "http://push2.eastmoney.com/api/qt/stock/get?ut=fa5opli0b&invt=2&fltt=2&fields=f57,f58,f116,f117,f167,f162,f163,f164,f47,f48,f46,f60,f127,f128,f129,f168,f44,f45&secid=" + _eastcode +"." + code + "&cb=jQuery112402603579518544119_1614885026385&_=" + str(
        _querynumber)
    try:
        r = requests.get(url=url)
    except:
        r = requests.get(url=url)
    res = json.loads(r.text.split('(', 1)[1].split(')')[0])
    a = res.get("data")
    #pd.read_json(a, orient='records')
    df = pd.DataFrame.from_records([a], index='f57')
    df.rename(index=mapping)
    df.rename(columns=mapping, inplace=True)
    return df


class MainHold:
    def __init__(self, name, id=0, date=0, number=0, value=0):
        self.name = name
        self.east_money_id = id
        self.hold = []
        self.date = date
        self.number = []
        self.value = []

    def add_to_hold(self, x, stockcode='', number=0, value=0):
        self.hold.append(x)
        self.stockcode.append(stockcode)
        self.number.append(number)
        self.value.append(value)



    # http://data.eastmoney.com/zlsj/2020-09-30-1-2.html
    # equity list
    # http://data.eastmoney.com/dataapi/zlsj/list?tkn=eastmoney&ReportDate=2020-09-30&code=&type=1&zjc=0&sortField=Count&sortDirec=1&pageNum=1&pageSize=50&cfg=jjsjtj
    # date in choice
    # http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/ZLSJBGQ/GetBGQ?tkn=eastmoney&sortDirec=1&pageNum=1&pageSize=25&cfg=zlsjbgq&js=jQuery1123015519727276562723_1615419097448&_=1615419097449
    # data for main holders
    # http://data.eastmoney.com/dataapi/zlsj/detail?SHType=&SHCode=&SCode=300059&ReportDate=2020-12-31&sortField=SHCode&sortDirec=1&pageNum=1&pageSize=30
    # main holder's data
    # http://fund.eastmoney.com/970016.html

class MainHold(MainHold):
    def __init__(self, name, id=0, date=0, number=0, value=0):
        self.name = name
        self.east_money_id = id
        self.date = date
        self.mainhold = MainHold(name, id, date)

    def add_to_hold(self, x, number=0, value=0):
        self.hold.append(x)
        self.number.append(x)
        self.value.append(x)

    def load_date(self):
        date_link = r'http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/ZLSJBGQ/GetBGQ?tkn=eastmoney&sortDirec=1&pageNum=1&pageSize=25&cfg=zlsjbgq&js=jQuery1123015519727276562723_1615419097448&_=1615419097449'
        try:
            r = requests.get(url=date_link)
            r.status_code
        except:
            print("failed to get dates")
        res = json.loads(r.text.split('(', 1)[1].split(')')[0])
        self.date = json.loads(json.dumps(res.get("Data")[0])).get("Data")



