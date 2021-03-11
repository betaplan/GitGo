import requests
import pandas as pd
import time
import json
import os
import csv
import numpy as np
import urllib.request

requests_path = r'http://data.eastmoney.com/zlsj/2020-09-30-1-2.html'



with urllib.request.urlopen(requests_path) as f:
    html = f.read().decode('utf-8')
print(html)

r = requests.get(requests_path)  # 抓取网页返回json信息
r.raise_for_status()
r.encoding = 'utf-8'

