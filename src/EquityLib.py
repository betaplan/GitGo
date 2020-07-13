import urllib
import requests
import pandas as pd
import time
import json
import datetime as dt
from tushare.stock import cons as ct
import os
from pandas import Series
from src.lib.SohuLib import download_stock_hist as download_sohu_hist
from src.lib.SohuLib import Get_stock_Background
import sys
sys.path.append('/easyquotation.easyquotation')
sys.path.append(r'C:\Users\ln_ti\PycharmProjects\GitGo\cn_stock_163')

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

class Market():
    def __init__(self):
        self.data = []
        self.pages = []
        self.url_list = []
        self.tickers = {}

    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)

    def prepare(self):
        self.get_pages_counts()
        self.get_url_lists(1,self.pages)
        self.get_tickers_ex(self.url_list)

    def get_pages_counts(self):
        # url = '''http://data.eastmoney.com/DataCenter_V3/jgdy/xx.ashx?pagesize=50&page=%d''' % 1
        # url += "&js=var%20ngDoXCbV&param=&sortRule=-1&sortType=0&rt=48753724"
        url = '''http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=%d''' % 1
        url += "&pageSize=20&js=var%20MuaZqltj={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1517270127528"
        wp = urllib.request.urlopen(url)
        # data = wp.read().decode('gbk')
        data = wp.read().decode('utf-8')
        data = data.replace('rank:', '\"rank\":').replace('pages:', '\"pages\":').replace('total:', '\"total\":')
        start_pos = data.index('=')
        json_data = data[start_pos + 1:]
        dict = json.loads(json_data)
        pages = dict['pages']
        # import urllib
        # jzc_html = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=1" \
        #            "&pageSize=20&js=var%20SGFWioRt={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1517274040425"
        # request = urllib.request.Request(jzc_html)
        # response = urllib.request.urlopen(request)
        # body = json.loads(response.read())
        self.pages = pages
        return pages

    def get_url_lists(self, start=1, end=1):
        url_list = []
        while (start <= end):
            url = '''http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=%d''' % start
            url += "&pageSize=20&js=var%20MuaZqltj={rank:[(x)],pages:(pc),total:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1517270127528"
            url_list.append(url)
            start += 1
        self.url_list = url_list
        return url_list

    def save_tickers(self):
        a_file = open("data.json", "w")
        json.dump(self.tickers, a_file)
        a_file.close()

    def load_tickers(self, data_name="data.json"):
        a_file = open(data_name, "r")
        self.tickers = a_file.read()
        return self.tickers

    def get_tickers_ex(self, url_list=[]):
        if(url_list==[]):
            url_list = self.url_list
        tickers = {}
        for index in range(len(url_list)):
            print(index)
            # if int(index/10)*10 == index:
            # try:
            try:
                url0 = urllib.request.urlopen(url_list[index])
                test_message = url0.read().decode('utf-8')
            except (urllib.error.HTTPError, ConnectionResetError):
                try:
                    time.sleep(2)
                    url0 = urllib.request.urlopen(url_list[index])
                    test_message = url0.read().decode('utf-8')
                except (urllib.error.HTTPError, ConnectionResetError):
                    try:
                        time.sleep(10)
                        url0 = urllib.request.urlopen(url_list[index])
                        test_message = url0.read().decode('utf-8')
                    except (urllib.error.HTTPError, ConnectionResetError):
                        print("url_list:", index, " failed")
            # test_message = requests.get(url=url0).decode('utf-8')
            start_pos = test_message.index('=')
            json_data = test_message[start_pos + 1:]
            json_data = json_data.replace('rank:', '\"rank\":').replace('pages:', '\"pages\":').replace('total:',
                                                                                                        '\"total\":')
            dict = json.loads(json_data)
            list = dict['rank']
            for index_list in range(len(list)):
                stock_info = list[index_list].split(',')
                if (stock_info[1][0]) == '6':
                    tickers[stock_info[1] + '.SS'] = stock_info[2]
                if (stock_info[1][0]) == '3':
                    tickers[stock_info[1] + '.SZ'] = stock_info[2]
                if (stock_info[1][0]) == '0':
                    tickers[stock_info[1] + '.SZ'] = stock_info[2]
            # except OSError:
            #     print("OSError", url_list[index],json_data)
        self.tickers = tickers
        return tickers

    def get_hist_data(self, code=None, start=None, end=None,
                      ktype='D', retry_count=3,
                      pause=0.001):
        """
            获取个股历史交易记录
        Parameters
        ------
          code:string
                      股票代码 e.g. 600848
          start:string
                      开始日期 format：YYYY-MM-DD 为空时取到API所提供的最早日期数据
          end:string
                      结束日期 format：YYYY-MM-DD 为空时取到最近一个交易日数据
          ktype：string
                      数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
          retry_count : int, 默认 3
                     如遇网络等问题重复执行的次数
          pause : int, 默认 0
                    重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
        return
        -------
          DataFrame
              属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率
        """
        symbol = ct._code_to_symbol(code)
        url = ''
        if ktype.upper() in ct.K_LABELS:
            url = ct.DAY_PRICE_URL % (ct.P_TYPE['http'], ct.DOMAINS['ifeng'],
                                      ct.K_TYPE[ktype.upper()], symbol)
        elif ktype in ct.K_MIN_LABELS:
            url = ct.DAY_PRICE_MIN_URL % (ct.P_TYPE['http'], ct.DOMAINS['ifeng'],
                                          symbol, ktype)
        else:
            raise TypeError('ktype input error.')

        for _ in range(retry_count):
            time.sleep(pause)
            try:
                request = Request(url)
                lines = urlopen(request, timeout=10).read()
                if len(lines) < 15:  # no data
                    return None
            except Exception as e:
                print(e)
            else:
                js = json.loads(lines.decode('utf-8') if ct.PY3 else lines)
                cols = []
                if (code in ct.INDEX_LABELS) & (ktype.upper() in ct.K_LABELS):
                    cols = ct.INX_DAY_PRICE_COLUMNS
                else:
                    cols = ct.DAY_PRICE_COLUMNS
                if len(js['record'][0]) == 14:
                    cols = ct.INX_DAY_PRICE_COLUMNS
                df = pd.DataFrame(js['record'], columns=cols)
                if ktype.upper() in ['D', 'W', 'M']:
                    df = df.applymap(lambda x: x.replace(u',', u''))
                    df[df == ''] = 0
                for col in cols[1:]:
                    df[col] = df[col].astype(float)
                if start is not None:
                    df = df[df.date >= start]
                if end is not None:
                    df = df[df.date <= end]
                if (code in ct.INDEX_LABELS) & (ktype in ct.K_MIN_LABELS):
                    df = df.drop('turnover', axis=1)
                df = df.set_index('date')
                df = df.sort_index(ascending=False)
                return df
        raise IOError(ct.NETWORK_URL_ERROR_MSG)

    import pandas as pd
    def download_stocks(self, tickers, folder):
        start = dt.datetime(2015, 1, 1)
        end = dt.datetime(2020, 7, 1)
        if not os.path.exists(folder):
            os.mkdir(folder)
        for ticker in tickers:
            # just in case your connection breaks, we'd like to save our progress!
            if not os.path.exists(folder + '/{}.csv'.format(ticker)):

                while True:
                    # try:
                    #     web.DataReader(ticker, "google", dt.datetime(2015, 1, 1), dt.datetime(2018, 2, 1))
                    # except IOError as err:
                    #     print("I/O error: {0}".format(err))
                    try:
                        # df = ts.get_h_data(ticker.split(".")[0], start='2015-01-01', end='2018-02-01')
                        df = self.get_hist_data(ticker.split(".")[0], start='2015-01-01', end='2020-06-01')
                        break
                    except IOError as err:
                        print("I/O error: {0}".format(err))
                    except ValueError:
                        print("Oops!   Try again...")
                # df = ts.get_h_data(ticker.split(".")[0], start='2015-01-01', end='2018-02-01')
                pd.DataFrame(df).to_csv(folder + '/{}.csv'.format(ticker))
            else:
                print('Already have {}'.format(ticker))
        return 1

    def download_Sohu_stocks(self, tickers, folder, start='20150101', end='20200709'):
        for ticker in tickers:
            print(ticker)
            if not os.path.exists(folder):
                os.mkdir(folder)
            filename = folder + '/{}.csv'.format(ticker)
            download_sohu_hist(ticker.split(".")[0], filename, start='20150101', end='20200708')

    def collect_stock_information(self, tickers, outfile='stockmarket.csv'):
        df = pd.DataFrame({'A' : []})
        for ticker in tickers:
            print(ticker)
            if df.empty:
                df = Get_stock_Background(ticker.split(".")[0])
            else:
                df = df.append(Get_stock_Background(ticker.split(".")[0]))
        df.to_csv(outfile)
        pickle = outfile[-3]+'pkl'
        df.to_pickle(pickle)

    def load_data_test(self, folder):
        return pd.read_csv(folder + '/{}.csv'.format('test'))
    #
    # folder = 'cn_stock'
    # download_stocks(list(cn_tickers.keys()), folder)

    def loadData(self, folder, assetId):
        try:
            return pd.read_csv(folder + '/{}.csv'.format(assetId))
        except:
            return "Failed"

    #
    # folder = 'cn_stock'
    # download_stocks(list(cn_tickers.keys()), folder)

    def debug(self):
        return("debug")

class Equity(Market):
    def __init__(self):
        self.data = []

def plotAll():
    aMarket = Market()
    cn_tickers = aMarket.get_tickers_ex(aMarket.get_url_lists(0,aMarket.get_pages_counts()))
    folder = 'cn_stock'
    df_total = []
    for ticker in list(cn_tickers.keys()):
        if not os.path.exists(folder + '/{}.csv'.format(ticker)):
            print("The Ticker {} not exist".format(ticker))
        else:
            # df = Series.from_csv(folder + '/{}.csv'.format(ticker))
            df = pd.read_csv(folder + '/{}.csv'.format(ticker))
            try:
                df.date = pd.to_datetime(df.date)
            except AttributeError:
                print("The Ticker {} have no data".format(ticker))
            else:
                df.index = df.date
                del df['date']
                tickerName = ticker + '.close'
                df = df.rename(columns={'close': tickerName})
                if (len(df_total) == 0):
                    df_total = df[tickerName].to_frame()
                else:
                    # print('add {}'.format(ticker))
                    df_total = df_total.merge(df[tickerName].to_frame(), left_index=True, right_index=True, how='outer')


a = Market()
# a.prepare()
# a.collect_stock_information(a.tickers)""
# a.download_Sohu_stocks(a.tickers,"cn_stock_sohu")



