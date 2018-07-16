
print(__doc__)

import os, sys
sys.path.append(os.path.join(os.path.abspath(''),"src"))
sys.path.append(os.path.join(os.path.abspath(''),"GitHubGo\code"))
sys.path.append(os.path.join(os.path.abspath(''),"GitHubGo\cn_stock_163"))

import time
import EquityLib as el
import tsdata as ts
import importlib
importlib.reload(ts)
# Author: Gael Varoquaux gael.varoquaux@normalesup.org
# License: BSD 3 clause

import datetime

import numpy as np
import matplotlib.pyplot as plt
try:
     from matplotlib.finance import quotes_historical_yahoo_ochl
except ImportError:
     # quotes_historical_yahoo_ochl was named quotes_historical_yahoo before matplotlib 1.4
     from matplotlib.finance import quotes_historical_yahoo as quotes_historical_yahoo_ochl
from matplotlib.collections import LineCollection
from sklearn import cluster, covariance, manifold

###############################################################################
# Retrieve the data from Internet

# Choose a time period reasonably calm (not too long ago so that we get
# high-tech firms, and before the 2008 crash)
market_data = el.Market()
d1 = datetime.datetime(2015, 1, 1)
d2 = datetime.datetime(2017, 4, 7)
filepath = "cn_stock_163"
import os
symbol_dict = {}
a_list = ['None','NaN']
for file in os.listdir(filepath):
    if file.endswith(".csv"):
        try:
            # print(os.path.join("cn_stock_163", file))
            test = market_data.loadData(filepath, file[:-4])['涨跌幅']
            None_notin = ('None' not in str(test))
            NaN_notin = ('NaN' not in str(test))
            if(None_notin and NaN_notin):
                # print(file, True in ((market_data.loadData(filepath,'603997.SS.csv'[:-4])['日期'])).isin(['2015-01-02']))
                if(True in ((market_data.loadData(filepath,file[:-4])['日期'])).isin(['2015-01-02'])):
                    if (True in ((market_data.loadData(filepath, file[:-4])['日期'])).isin(['2018-01-02'])):
                        if (True in ((market_data.loadData(filepath, file[:-4])['日期'])).isin(['2017-01-03'])):
                            if (True in ((market_data.loadData(filepath, file[:-4])['日期'])).isin(['2018-03-26'])):
                                if (True in ((market_data.loadData(filepath, file[:-4])['日期'])).isin(['2018-03-27'])):
                                    symbol_dict[file[:-4]] = market_data.loadData(filepath,file[:-4])['名称'][0]
        except:
            print(file)

# kraft symbol has now changed from KFT to MDLZ in yahoo
# symbol_dict = {
#     # '000001.SS': 'Total',
#     '600718.SS': 'Dong ruan',
#     '600100.SS': 'Tong fang',
#     '601111.SS': 'AIR CHINA',
#     '600029.SS': 'South CHINA',
#     '600104.SS': 'Shang qi',
#     '601318.SS': 'Pingan China',
#     '601398.SS': 'ICBC',
#     '600050.SS': 'China U',
#     '600026.SS': 'zhongyuan haineng',
#     '600795.SS': 'guo dian',
#     '601166.SS': 'xingxie bank',
#     '601288.SS': 'nongye bank',
#     '600177.SS': 'ya ge er',
#     '600690.SS': 'hai er',
#     '000333.SZ': 'meidi',
#     '000651.SZ': 'geli',
#     '601872.SS': 'zhao shang chuan',
#     '600000.SS': 'shpd',
#     '600129.SS': 'taiji'}

symbols, names = np.array(list(symbol_dict.items())).T

print(len(symbol_dict))
# quotes = [quotes_historical_yahoo_ochl(symbol, d1, d2, asobject=True)
#           for symbol in symbols]
from pandas_datareader import data

quotes = [market_data.loadData('cn_stock_163',symbol)
          for symbol in symbols]
columnNames = ['Date','id','name','close','high','low','open',
           'pre-close','variation','return','changeRatio',
           'tradingVol','cashVol','marketValue','liveValue']
columnsNames={'日期':'Date', '股票代码':'id', '名称':'name', '收盘价':'close', '最高价':'high',
                  '最低价':'low','开盘价': 'open', '前收盘':'pre-close', '涨跌额':'variation', '涨跌幅':'return',
                  '换手率':'changeRatio', '成交量':'tradingVol','成交金额': 'cashVol', '总市值':'marketValue', '流通市值':'liveValue'}
# a.rename(columns={'日期':'Date', '股票代码':'id', '名称':'name', '收盘价':'close', '最高价':'high',
#                   '最低价':'low','开盘价': 'open', '前收盘':'pre-close', '涨跌额':'variation', '涨跌幅':'return',
#                   '换手率':'changeRatio', '成交量':'tradingVol','成交金额': 'cashVol', '总市值':'marketValue', '流通市值':'liveValue'}, inplace = True)
[q.rename(columns=columnsNames, inplace = True) for q in quotes]
testdata = ts.tsdata()
for isin, q in zip(symbols, quotes):
    testdata.insetData(isin,q)
    print(time.strftime('%H:%M:%S'), isin)

for name, data  in zip(testdata.colNames, testdata.dataFrames):
    data.to_csv( 'data/{}.csv'.format(name))

testdata.dataFrames[0].head(10)
print(testdata.find(['close','open']))
    # fdata = testdata.importData(quotes[0])

import correlandplot as crp
df = testdata.dataFrames[testdata.find(['return'])[0]]
ddf = testdata.dataFrames[testdata.find(['pre-close'])[0]]
d1 = datetime.datetime(2015, 1, 1)
df =df[df.index > d1]
ddf =ddf[ddf.index > d1]
df0 = df / ddf
df =df.replace('None', np.nan)
df = df.replace('NaN', np.nan)
df = df.replace(np.nan, 0)
print(df)
crp.dataAnalysis(np.asarray(df).astype(np.float).T,np.asarray(testdata.colId))

##print([q.open for q in quotes])
# open = np.array([q.open for q in quotes]).astype(np.float)
# close = np.array([q.close for q in quotes]).astype(np.float)
#
# # The daily variations of the quotes are what carry most information
# variation = close - open