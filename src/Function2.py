
print(__doc__)

import os, sys
sys.path.append(r"C:\Users\home\PycharmProjects\GitGo")
sys.path.append(r"..")
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

# kraft symbol has now changed from KFT to MDLZ in yahoo
symbol_dict = {
    # '000001.SS': 'Total',
    '000001.SZ': '平安银行',
    '000036.SZ': '华联控股',
    '000039.SZ': '中集集团',
    '000059.SZ': '华锦股份',
    '000063.SZ': '中兴通讯',
    '000100.SZ': 'TCL集团',
    '000150.SZ': '宜华健康',
    '000333.SZ': '美的集团',
    '000338.SZ': '潍柴动力',
    '000501.SZ': '鄂武商A',
    '000600.SZ': '建投能源',
    '000625.SZ': '长安汽车',
    '000651.SZ': '格力电器',
    '000719.SZ': '中原传媒',
    '000725.SZ': '京东方A',
    '000776.SZ': '广发证券',
    '000826.SZ': '启迪桑德',
    '000848.SZ': '承德露露',
    '000869.SZ': '张裕A',
    '000881.SZ': '中广核技',
    '000895.SZ': '双汇发展',
    '000938.SZ': '紫光股份',
    '000977.SZ': '浪潮信息',
    '000999.SZ': '华润三九',
    '002013.SZ': '中航机电',
    '002019.SZ': '亿帆医药',
    '002048.SZ': '宁波华翔',
    '002202.SZ': '金风科技',
    '002203.SZ': '海亮股份',
    '002236.SZ': '大华股份',
    '002301.SZ': '齐心集团',
    '002304.SZ': '洋河股份',
    '002310.SZ': '东方园林',
    '002415.SZ': '海康威视',
    '002446.SZ': '盛路通信',
    '002450.SZ': '康得新',
    '002472.SZ': '双环传动',
    '002501.SZ': '利源精制',
    '002502.SZ': '骅威文化',
    '002594.SZ': '比亚迪',
    '002699.SZ': '美盛文化',
    '002714.SZ': '牧原股份',
    '002739.SZ': '万达电影',
    '300065.SZ': '海兰信',
    '300118.SZ': '东方日升',
    '300136.SZ': '信维通信',
    '300138.SZ': '晨光生物',
    '300145.SZ': '中金环境',
    '300146.SZ': '汤臣倍健',
    '300156.SZ': '神雾环保',
    '300171.SZ': '东富龙',
    '300197.SZ': '铁汉生态',
    '300199.SZ': '翰宇药业',
    '300207.SZ': '欣旺达',
    '300251.SZ': '光线传媒',
    '300271.SZ': '华宇软件',
    '300310.SZ': '宜通世纪',
    '300408.SZ': '三环集团',
    '300433.SZ': '蓝思科技',
    '600000.SS': '浦发银行',
    '600011.SS': '华能国际',
    '600019.SS': '宝钢股份',
    '600023.SS': '浙能电力',
    '600026.SS': '中远海能',
    '600027.SS': '华电国际',
    '600029.SS': '南方航空',
    '600030.SS': '中信证券',
    '600050.SS': '中国联通',
    '600056.SS': '中国医药',
    '600060.SS': '海信电器',
    '600072.SS': '中船科技',
    '600079.SS': '人福医药',
    '600100.SS': '同方股份',
    '600104.SS': '上汽集团',
    '600129.SS': '太极集团',
    '600133.SS': '东湖高新',
    '600177.SS': '雅戈尔',
    '600196.SS': '复星医药',
    '600229.SS': '城市传媒',
    '600240.SS': '华业资本',
    '600276.SS': '恒瑞医药',
    '600309.SS': '万华化学',
    '600352.SS': '浙江龙盛',
    '600354.SS': '敦煌种业',
    '600362.SS': '江西铜业',
    '600366.SS': '宁波韵升',
    '600372.SS': '中航电子',
    '600398.SS': '海澜之家',
    '600487.SS': '亨通光电',
    '600519.SS': '贵州茅台',
    '600522.SS': '中天科技',
    '600584.SS': '长电科技',
    '600585.SS': '海螺水泥',
    '600587.SS': '新华医疗',
    '600642.SS': '申能股份',
    '600660.SS': '福耀玻璃',
    '600674.SS': '川投能源',
    '600685.SS': '中船防务',
    '600690.SS': '青岛海尔',
    '600697.SS': '欧亚集团',
    '600699.SS': '均胜电子',
    '600718.SS': '东软集团',
    '600741.SS': '华域汽车',
    '600795.SS': '国电电力',
    '600823.SS': '世茂股份',
    '600826.SS': '兰生股份',
    '600835.SS': '上海机电',
    '600887.SS': '伊利股份',
    '600893.SS': '航发动力',
    '601006.SS': '大秦铁路',
    '601088.SS': '中国神华',
    '601111.SS': '中国国航',
    '601166.SS': '兴业银行',
    '601186.SS': '中国铁建',
    '601211.SS': '国泰君安',
    '601238.SS': '广汽集团',
    '601288.SS': '农业银行',
    '601311.SS': 'XD骆驼股',
    '601318.SS': '中国平安',
    '601398.SS': '工商银行',
    '601600.SS': '中国铝业',
    '601607.SS': '上海医药',
    '601611.SS': '中国核建',
    '601628.SS': '中国人寿',
    '601633.SS': '长城汽车',
    '601668.SS': '中国建筑',
    '601766.SS': '中国中车',
    '601872.SS': '招商轮船',
    '601899.SS': '紫金矿业',
    '601919.SS': '中远海控',
    '601928.SS': '凤凰传媒',
    '601939.SS': '建设银行',
    '601985.SS': '中国核电',
    '601988.SS': '中国银行',
    '601989.SS': '中国重工',
    '603598.SS': '引力传媒',}

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
importlib.reload(crp)
df = testdata.dataFrames[testdata.find(['return'])[0]]
d1 = datetime.datetime(2015, 1, 1)
df =df[df.index > d1]
df =df.replace('None', np.nan)
df = df.replace('NaN', np.nan)
df = df.replace(np.nan, 0)
print(df)
crp.dataAnalysis(np.asarray(df).astype(np.float).T,names)

##print([q.open for q in quotes])
# open = np.array([q.open for q in quotes]).astype(np.float)
# close = np.array([q.close for q in quotes]).astype(np.float)
#
# # The daily variations of the quotes are what carry most information
# variation = close - open

import matplotlib
print(matplotlib.matplotlib_fname())