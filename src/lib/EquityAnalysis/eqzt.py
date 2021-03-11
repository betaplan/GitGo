from src.EquityLib import Market
from src.tsdata import tsdata
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
folder = "./cn_stock_sohu"

loaddata = Market()
loaddata.load_tickers()
tickers_name = list(json.loads(loaddata.tickers).keys())
matrixdata = tsdata()
for i in tickers_name:
    print(i)
    filename = folder + '/{}.csv'.format(i)
    matrixdata.insetData(i.split(".")[0], filename)

matrixdata.dataFrames[0]
assetname = "600893.SS"
filename = folder + '/{}.csv'.format(assetname)
matrixdata.insetData(assetname.split(".")[0], filename)
assetname = "000001.SZ"
assetname = "300773.SZ"
filename = folder + '/{}.csv'.format(assetname)
matrixdata.importData(filename)
assetname = '688009.SS'

matrixdata.dataFrames[0].head(1)[matrixdata.dataFrames[0].head(1).notna()]
matrixdata.dataFrames[0].head(1).dropna(axis=1)

import pandas as pd
assetname = "300773.SZ"
filename = folder + '/{}.csv'.format(assetname)
input_data3 = pd.read_csv(filename, encoding="gbk", index_col=False)
input_data3


import pandas as pd
assetname = '688009.SS'
filename = folder + '/{}.csv'.format(assetname)
input_data3 = pd.read_csv(filename, encoding="gbk", index_col=False)
input_data3

matrixdata.dataFrames[1].dropna(axis=1,how='all')
matrixdata.dataFrames[1].bfill().ffill().dropna()
matrixdata.dataFrames[1].bfill().ffill().corr(method='pearson', min_periods=1)
matrixdata.dataFrames[1].dropna(axis=1,how='all').bfill().ffill().corr(method='pearson', min_periods=1)

