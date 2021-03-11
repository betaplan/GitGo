import requests
import re
from multiprocessing import Pool
import json
import csv
import pandas as pd
import os
import time

path = r'http://31.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'


def get_json(url):  # 获取JSON
    try:
        r = requests.get(url)  # 抓取网页返回json信息
        r.raise_for_status()
        r.encoding = 'utf-8'
        # print(r.json())
        # with open(r"C:\Users\xxp\.spyder-py3\testcode\tmp.txt", "w") as fp:
        # fp.write(json.dumps(r.json(),indent=4,ensure_ascii=False)) # txt测试是否成功获取网页
        return r.json()
    except:
        return 'false'

result = get_json(path)
items_all = []
all_name = result.get("data").get("diff")  # list类型
    for i in range(0, len(all_name) - 1):  # 数组长度限定30交易日内数据
        item = all_name[i]  # 获取数据 dict类型
        items_all += [item['f12']]
