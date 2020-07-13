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
    filename = folder + '/{}.csv'.format(i)
    matrixdata.insetData(i.split(".")[0], filename)

