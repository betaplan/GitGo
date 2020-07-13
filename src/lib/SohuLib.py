import urllib
import requests
import pandas as pd
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
codebook = { "0": "SZ",
             "6": "SS",
             "3": "SZ",
             }

dirlocation = os.path.dirname(os.path.abspath(__file__))

cur_folder = dirlocation +'\\cn_stock_sohu\\'

def Get_stock_Background(code = '000001'):
    # url = '''http://data.eastmoney.com/DataCenter_V3/jgdy/xx.ashx?pagesize=50&page=%d''' % 1
    # url += "&js=var%20ngDoXCbV&param=&sortRule=-1&sortType=0&rt=48753724"
    # importing the requests library

    _querynumber = random.randrange(1000000000)
    _rightthree = code[-3:]
    URL = "https://hq.stock.sohu.com/cn/" + _rightthree +"/cn_" + code + "-1.html?_=" + str(_querynumber)
    r = requests.get(url=URL)
    str_r = r.text[11:-2].replace("\'", "\"").strip("'<>() ") \
        .replace("\"[\"", "\"[\'").replace("\"]\"", "\']\"").replace("\",\"", "\',\'").replace("\"],[\"","\'],[\'")
    try:
        res = json.loads(str_r)
        # ############################# Here we load price A1 as default df ############################
        data_string = "\"" + res['price_A1'][0].replace("\'", "\"")[1:-1] + "\""
        data = io.StringIO(data_string)
        df = pd.read_csv(data, sep=",", header=None)
        df.columns = ['0-ID', '0-Name', '0-Close', '0-Change', '0-Percentage', '0-A1', '0-A2', '0-A3']
        # ############################# Here we load time ############################
        data_string = res['time'][0].replace("\'", "")
        df['DateTime'] = datetime.strptime(data_string,'%Y,%m,%d,%H,%M,%S')
        # ############################# Here we load price A2 to df ############################
        data_string = "\"" + res['price_A2'][0].replace("\'", "\"")[1:-1] + "\""
        data = io.StringIO(data_string)
        df_temp = pd.read_csv(data, sep=",", header=None)
        df_temp.columns = ['1-AveragePrice', '1-YesterdayClose', '1-CurrentPosition',\
        '1-TodayOpen', '1-量比', '1-High', '1-换手率', '1-Low', '1-总手',\
                           '1-涨停','1-市盈率','1-跌停','1-总金额','1-CurrentPrice','1-振幅','1-B1']
        df = pd.concat([df, df_temp], axis=1)
        # ############################# Here we load sector ############################
        try:
            data_string = "[\"" + res['sector'][0][0].replace("\'", "\"")[1:-1] + "\"]"
            data = io.StringIO(data_string)
            df_temp = pd.read_csv(data, sep=",", header=None)
            for i in range(int(len(df_temp.columns)/4)):
                df[df_temp[i*4+1][0]]=df_temp[i*4+2][0]
        except IndexError:
            print(code, " Have no sector.")
    except ValueError:
        d = {'ID': [code]}
        df = pd.DataFrame(data=d)
    return df

def download_stock_hist(code='000001', filename = '000001.csv', start='20150101', end='20200706'):
    url = 'http://q.stock.sohu.com/hisHq?code=cn_' \
    + code + '&start=' \
    + start + '&end=' \
    + end + '&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp&r=0.543412915586595&0.7723848901142324'
    html = urllib.request.urlopen(url).read()
    html = html.decode('gbk')
    html = html[21:-2]  # 去BOM头
    data = json.loads(html)
    try:
        datalist = data[0]['hq']
    except KeyError:
        datalist = []
    # market_code = codebook[code[:1]]
    # filename = cur_folder + market_code + code + '.csv'
    filetitle = ["日期", "开盘", "收盘", "涨跌额", "涨跌幅", "最低", "最高", "成交量(手)", "成交金额(万)", "换手率"]

    with open(filename, "w", newline='') as csvFile:
        csv_writer = csv.writer(csvFile)
        csv_writer.writerow(filetitle)
        for data in datalist:
            csv_writer.writerow(data)
        csvFile.close


    # marketcode = codebook[code[:1]]
    # import requests
    # url = 'https://q.stock.sohu.com/qp/hq?type=snapshot&code=%s&set='
    # url += marketcode + code
    # wp = urllib.request.urlopen(url)
    # response = requests.get('https://api.github.com')
    # data = response.content.encoding = 'gbk'
    # # data = wp.read().decode('gbk')
    # # data = str(wp.read(), 'gbk')
    # f = open('workfile', 'w')
    # f.write(data)
    # f.close()
    # from bs4 import BeautifulSoup
    # soup = BeautifulSoup(data, 'html.parser')
    # soupmid = soup.find(name='table', attrs={"id":"FT_priceA2"})
    # for tag in soup.find_all(name='div',attrs={"class":"rightTop clearfix"}):
    #     print(tag.string)
    # for table in soup.find_all('table'):
    #     table_rows = table.find_all('tr')
    #     for tr in table_rows:
    #         td = tr.find_all('td')
    #         row = [i.text for i in td]
    #         print(row)
    # requst0 = "https://hq.stock.sohu.com/cn/001/cn_000001-1.html?_=1594069562321"
    # headers = {
    #     ":authority": "hq.stock.sohu.com",
    #     ":method": "GET",
    #     ":path": "/cn/001/cn_000001-1.html?_=1594069562321",
    #     ":scheme": "https",
    #     "accept": "*/*",
    #     "accept-encoding": "gzip, deflate, br",
    #     "accept-language": "zh-CN,zh;q=0.9",
    #     "cookie": "SUV=15889560469056j7lh2; gidinf=x099980109ee1178270951c0f000ec0b0fcc0b6b8a4a; debug_test=sohu_third_cookie; IPLOC=GB; BIZ_MyLBS=cn_000001%2C%u5E73%u5B89%u94F6%u884C%7C; t=1594061207841; reqtype=pc",
    #     "referer": "https://q.stock.sohu.com/qp/hq?type=snapshot&code=%s&set=zs00000",
    #     "sec-fetch-dest": "script",
    #     "sec-fetch-mode": "no-cors",
    #     "sec-fetch-site": "same-site",
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    # }

    # link = 'http://q.stock.sohu.com/qp/hq?type=snapshot&code=%s&set=zs000001'
    # import requests
    # response = requests.get(link)
    # response.encoding = 'gbk'
    # data = response.text
    # print(data)
    # data = data.replace('rank:', '\"rank\":').replace('pages:', '\"pages\":').replace('total:', '\"total\":')
    # start_pos = data.index('=')
    # json_data = data[start_pos + 1:]
    # dict = json.loads(json_data)
    # pages = dict['pages']
    #
    # return data