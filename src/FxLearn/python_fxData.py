# -*- coding: utf-8 -*-
"""
Created on Thu Dec 08 15:46:59 2016
@author: fxcm
"""
##from StringIO import StringIO
import os
from io import BytesIO
import gzip
import urllib
import datetime
import  shutil
import pandas as pd
import pathlib
import sys
import io
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO


def LoadFX(FXFolderpath,year,symbol,i,url_suffix,url ):
    zipfle_name = FXFolderpath + '/' + str(year) + '/' + symbol + '-' + str(i) + url_suffix
    if(os.path.exists(zipfle_name)):
        with open(zipfle_name, 'rb') as fin:
             data = BytesIO(fin.read())
        fin.close()
    else:
        url_data = url + symbol + '/' + str(year) + '/' + str(i) + url_suffix
        print(url_data)
        requests = urllib.request.urlopen(url_data)
        data = BytesIO(requests.read())
        with urllib.request.urlopen(url_data) as response, open(zipfle_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    # print("data ready")
    return data

url = 'https://tickdata.fxcorporate.com/'##This is the base url
url_suffix = '.csv.gz' ##Extension of the file name
symbol = 'EURUSD' ##symbol we want to get tick data for
FXFolderpath = r'src/data/fx'


##Available Currencies
##AUDCAD,AUDCHF,AUDJPY, AUDNZD,CADCHF,EURAUD,EURCHF,EURGBP
##EURJPY,EURUSD,GBPCHF,GBPJPY,GBPNZD,GBPUSD,GBPCHF,GBPJPY
##GBPNZD,NZDCAD,NZDCHF.NZDJPY,NZDUSD,USDCAD,USDCHF,USDJPY

###The URL is a combination of the currency, year, and week of the year.
###Example URL https://tickdata.fxcorporate.com/EURUSD/2015/29.csv.gz
###The example URL should be the first URL of this example

##This will loop through the weeks needed, create the correct URL and print out the lenght of the file.
symbol = 'EURUSD' ##symbol we want to get tick data for
def prepare_FX(symbol,returntype,start_dt=datetime.date(2015, 1, 1),end_dt = datetime.date(2018, 8, 13)):
    returnType = returntype.split(",")
    url = 'https://tickdata.fxcorporate.com/'  ##This is the base url
    url_suffix = '.csv.gz'  ##Extension of the file name
    FXFolderpath = r'data/fx'
    ##The tick files are stored a compressed csv.  The storage structure comes as {symbol}/{year}/{week_of_year}.csv.gz
    ##The first week of the year will be 1.csv.gz where the
    ##last week might be 52 or 53.  That will depend on the year.
    ##Once we have the week of the year we will be able to pull the correct file with the data that is needed.

    start_wk = start_dt.isocalendar()[1]  ##find the week of the year for the start
    end_wk = end_dt.isocalendar()[1]  ##find the week of the year for the end
    start_year = str(start_dt.isocalendar()[0])  ##pull out the year of the start
    end_year = str(end_dt.isocalendar()[0])  ##pull out the year of the start
    df = []
    for y in range(int(start_year), int(end_year)+1):
        year = y
        print(year,int(start_year), int(end_year)+1)
        if year == int(start_year):
            firstDayWek = start_wk
        else:
            firstDayWek = 1
        if year == int(end_year):
            lastDayWek = end_wk
        else:
            lastDayWek = datetime.date(year, 12, 31).isocalendar()[1]
        pathlib.Path(FXFolderpath + '/' + str(year)).mkdir(parents=True, exist_ok=True)
        filename = FXFolderpath + '/' + str(year)  + '/' + symbol + '.csv'
        print(firstDayWek, lastDayWek, filename)

        with open(filename, "w") as text_file:
            for i in range(firstDayWek, lastDayWek ):
                buf = LoadFX(FXFolderpath,year,symbol,i,url_suffix,url )
                f = gzip.GzipFile(fileobj=buf)
                if "f" in returntype:
                    text_file.write(f.read().decode("utf-16"))
                if "pd" in returntype:
                    # print("pd")
                    data = (f.read().decode("utf-16"))
                    # print("decode")
                    df1=pd.read_csv(StringIO(data))
                    # print("Read to PD")
                    df1['DateTime'] = pd.to_datetime(df1['DateTime'])
                    # print("to_datetime")
                    if(1==len(returnType)):
                        try:
                            df = pd.concat([df,df1])
                        except TypeError:
                            df = df1
                    if (2 == len(returnType)):
                        print("returnType == 2")
                        df1 = df1.set_index('DateTime')
                        Bid = df1.Bid.resample(returnType[1]).ohlc()
                        Bidstd = df1.Bid.resample(returnType[1]).std()
                        Bid = pd.concat([Bid, Bidstd], axis=1)
                        Bid = Bid.rename(columns={"open": "openBid","high": "highBid", "low": "lowBid", "close": "closeBid",
                                                  "Bid": "stdBid" })
                        Ask = df1.Ask.resample(returnType[1]).ohlc()
                        Askstd = df1.Ask.resample(returnType[1]).std()
                        Ask = pd.concat([Ask, Askstd], axis=1)
                        Ask = Ask.rename(columns={"open": "openAsk", "high": "highAsk", "low": "lowAsk", "close": "closeAsk",
                                     "Ask": "stdAsk"})
                        df1 = pd.concat([Bid, Ask], axis=1)
                        values = {'stdBid': 0, 'stdAsk': 0}
                        df1 = df1.fillna(value=values)
                        df1 = df1.fillna(method='ffill')
                        try:
                            df = pd.concat([df, df1])
                        except TypeError:
                            print("first file load")
                            df = df1
        text_file.close
    return df


def get_FX(symbol,returntype,start_dt=datetime.date(2015, 1, 1),end_dt = datetime.date(2018, 8, 13)):
    returnType = returntype.split(",")
    url = 'https://tickdata.fxcorporate.com/'  ##This is the base url
    url_suffix = '.csv.gz'  ##Extension of the file name
    FXFolderpath = r'data/fx'
    ##The tick files are stored a compressed csv.  The storage structure comes as {symbol}/{year}/{week_of_year}.csv.gz
    ##The first week of the year will be 1.csv.gz where the
    ##last week might be 52 or 53.  That will depend on the year.
    ##Once we have the week of the year we will be able to pull the correct file with the data that is needed.

    start_wk = start_dt.isocalendar()[1]  ##find the week of the year for the start
    end_wk = end_dt.isocalendar()[1]  ##find the week of the year for the end
    start_year = str(start_dt.isocalendar()[0])  ##pull out the year of the start
    end_year = str(end_dt.isocalendar()[0])  ##pull out the year of the start
    df = []
    for y in range(int(start_year), int(end_year)+1):
        year = y
        print(year,int(start_year), int(end_year)+1)
        if year == int(start_year):
            firstDayWek = start_wk
        else:
            firstDayWek = 1
        if year == int(end_year):
            lastDayWek = end_wk
        else:
            lastDayWek = datetime.date(year, 12, 31).isocalendar()[1]
        pathlib.Path(FXFolderpath + '/' + str(year)).mkdir(parents=True, exist_ok=True)
        filename = FXFolderpath + '/' + str(year)  + '/' + symbol + '.csv'
        print(firstDayWek, lastDayWek, filename)

        with open(filename, "w") as text_file:
            for i in range(firstDayWek, lastDayWek ):
                buf = LoadFX(FXFolderpath,year,symbol,i,url_suffix,url )
                f = gzip.GzipFile(fileobj=buf)
                if "f" in returntype:
                    text_file.write(f.read().decode("utf-16"))
                if "pd" in returntype:
                    data = (f.read().decode("utf-16"))
                    df1=pd.read_csv(StringIO(data))
                    df1['DateTime'] = pd.to_datetime(df1['DateTime'])
                    if(1==len(returnType)):
                        try:
                            df = pd.concat([df,df1])
                        except TypeError:
                            df = df1
                    if (2 == len(returnType)):
                        df1 = df1.set_index('DateTime')
                        Bid = df1.Bid.resample(returnType[1]).ohlc()
                        Bidstd = df1.Bid.resample(returnType[1]).std()
                        Bid = pd.concat([Bid, Bidstd], axis=1)
                        Bid = Bid.rename(columns={"open": "openBid","high": "highBid", "low": "lowBid", "close": "closeBid",
                                                  "Bid": "stdBid" })
                        Ask = df1.Ask.resample(returnType[1]).ohlc()
                        Askstd = df1.Ask.resample(returnType[1]).std()
                        Ask = pd.concat([Ask, Askstd], axis=1)
                        Ask = Ask.rename(columns={"open": "openAsk", "high": "highAsk", "low": "lowAsk", "close": "closeAsk",
                                     "Ask": "stdAsk"})
                        df1 = pd.concat([Bid, Ask], axis=1)
                        values = {'stdBid': 0, 'stdAsk': 0}
                        df1 = df1.fillna(value=values)
                        df1 = df1.fillna(method='ffill')
                        try:
                            df = pd.concat([df, df1])
                        except TypeError:
                            df = df1
        text_file.close
    return df

aa = prepare_FX("GBPUSD","pd,60S",datetime.date(2016, 1, 1),datetime.date(2016, 1, 31))
a = prepare_FX("GBPUSD","pd,1S",datetime.date(2015, 1, 1),datetime.date(2016, 1, 31))
aa.to_csv(r'data/fx/GBPUSD.csv')
b=pd.read_csv(r'data/fx/GBPUSD.csv')
b.iloc[0:9999].plot(y='openBid')
print(a)

