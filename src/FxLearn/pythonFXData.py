import numpy as np
import pandas as pd
import datetime as datetime
import pathlib
import os
from io import BytesIO
import gzip
import urllib
import datetime
import shutil
import pandas as pd
import pathlib
import sys
import io

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
trueFX = r'https://www.truefx.com/dev/data/2019/2019-01/AUDJPY-2019-01.zip'
pepperstone = r'https://www.truefx.com/dev/data//2016/NOVEMBER-2016/GBPUSD-2016-11.zip'
ratedataGaincapital = r'http://ratedata.gaincapital.com/2018/12%20December/GBP_USD_Week1.zip'
filename = r'C:\Users\home\PycharmProjects\GitGo\src\data\fx\2018\a.csv'
my_data = pd.read_csv(filename, '\t')
my_data['DateTime'] = pd.to_datetime(my_data['DateTime'])


# print(my_data)
# print(my_data.Bid)
def prepare_trainData(symbol, returntype, tWindow=[-60, 10], \
                      step='m', stepMulti=10, \
                      start_dt=datetime.date(2017, 1, 5), end_dt=datetime.date(2017, 1, 10)):
    data = get_trainData(symbol, returntype, start_dt, end_dt)
    data["DateTime"] = pd.to_datetime(data["DateTime"])
    print(type(data))
    print(len(data))
    tWindowa = np.timedelta64(tWindow[0] * 60, 's')
    print(data.DateTime.iloc[0])
    print(type(data.DateTime.iloc[0]))
    tTarget_start = data.DateTime.iloc[0] - tWindowa
    tWindowb = np.timedelta64(tWindow[1] * 60, 's')
    tTarget_end = data.DateTime.iloc[-1] - tWindowb
    tTarget = tTarget_start
    x_data = []
    y_data = []
    while tTarget < tTarget_end:
        print(tTarget)
        x_data.append(np.asarray(get_timedeltaData(data, tTarget, tWindow[0]*1000*60)))
        y_data.append(np.asarray(get_timedeltaData(data, tTarget, tWindow[1]*1000*60)))
        tTarget += np.timedelta64(stepMulti * 60, 's')
    # x_data = np.asarray(x_data)
    # y_data = np.asarray(y_data)
    return (x_data, y_data)


def get_timedeltaData(pandasData, tTarget, tWindow):
    tTarget = pd.to_datetime(tTarget)
    # tTarget = pd.to_datetime('2018-01-01 23:00:28.378')
    my_data = pandasData.copy()
    my_data.DateTime = ((my_data.DateTime - tTarget) / np.timedelta64(1, 'ms')).astype(int)
    if (tWindow < 0):
        return my_data[(my_data['DateTime'] > tWindow) & (my_data['DateTime'] <= 0)]
    else:
        return my_data[(my_data['DateTime'] < tWindow) & (my_data['DateTime'] >= 0)]


def get_trainData(symbol, returntype, start_dt=datetime.date(2017, 1, 1), end_dt=datetime.date(2018, 8, 13)):
    returnType = returntype.split(",")
    ##Extension of the file name
    url_suffix = r'.csv.gz'
    FXFolderpath = r'data/fx'
    ##The tick files are stored a compressed csv.  The storage structure comes as {symbol}/{year}/{week_of_year}.csv.gz
    ##The first week of the year will be 1.csv.gz where the
    ##last week might be 52 or 53.  That will depend on the year.
    ##Once we have the week of the year we will be able to pull the correct file with the data that is needed.
    print("start_dt", start_dt)
    print("end_dt", end_dt)

    start_wk = start_dt.isocalendar()[1]  ##find the week of the year for the start
    end_wk = end_dt.isocalendar()[1]  ##find the week of the year for the end
    start_year = str(start_dt.isocalendar()[0])  ##pull out the year of the start
    end_year = str(end_dt.isocalendar()[0])  ##pull out the year of the start
    df = []
    for y in range(int(start_year), int(end_year) + 1):
        year = y
        print(year, int(start_year), int(end_year) + 1)
        if year == int(start_year):
            firstDayWek = start_wk
        else:
            firstDayWek = 1
        if year == int(end_year):
            lastDayWek = end_wk
        else:
            lastDayWek = datetime.date(year, 12, 31).isocalendar()[1]
        pathlib.Path(FXFolderpath + '/' + str(year)).mkdir(parents=True, exist_ok=True)
        filename = FXFolderpath + '/' + str(year) + '/' + symbol + '.csv'
        print("firstDayWek,lastDayWek", firstDayWek, lastDayWek)
        for i in range(firstDayWek, lastDayWek):
            buf = LoadFX(FXFolderpath, year, symbol, i, url_suffix, url)
            print("load FX", year, i)
            f = gzip.GzipFile(fileobj=buf)
            if "pd" in returntype:
                data = (f.read().decode("utf-16"))
                df1 = pd.read_csv(StringIO(data))
                print("df1 read csv")
                df1['DateTime'] = pd.to_datetime(df1['DateTime'], format="%m/%d/%Y %H:%M:%S.%f")
                print("df1 to_datetime")
                try:
                    df = pd.concat([df, df1])
                except TypeError:
                    df = df1
    return df


def LoadFX(FXFolderpath, year, symbol, i, url_suffix, url):
    zipfle_name = FXFolderpath + '/' + str(year) + '/' + symbol + '-' + str(i) + url_suffix
    if (os.path.exists(zipfle_name)):
        with open(zipfle_name, 'rb') as fin:
            data = BytesIO(fin.read())
        fin.close()
    else:
        url_data = url + symbol + '/' + str(year) + '/' + str(i) + url_suffix
        print(url_data)
        requests = urllib.request.urlopen(url_data)
        data = BytesIO(requests.read())
        shutil.copyfileobj(response, out_file)
    return data

def numpy_fillna(data):
    # Get lengths of each row of data
    lens = np.array([len(i) for i in data])

    # Mask of valid places in each row
    mask = np.arange(lens.max()) < lens[:,None]

    # Setup output array and put elements from data into masked positions
    zeroshape = list(mask.shape)
    zeroshape.extend([3])
    try:
    	out = np.zeros(zeroshape, dtype=data.dtype)
    except:
    	out = np.zeros(zeroshape, dtype=data[0].dtype)
    # for i in range(len(data)):
    # 	out[i][mask[i]] = data[i]
    out[mask] = np.concatenate(data)
    return out

def dataLogReturn(data):
    axis = len(data.shape) - 2
    output = np.diff(np.log(data), axis=axis)
    output[np.isneginf(output)] = 0
    output[np.isnan(output)] = 0
    timeR = np.sqrt(np.diff(data, axis=1))
    output[:, :, 1] = output[:, :, 1] / timeR[:, :, 0]
    output[:, :, 2] = output[:, :, 2] / timeR[:, :, 0]
    output[np.isnan(output)] = 0
    return output

def fit_to_lognormal(b):
    sigma = np.std(np.log(b))
    mu = np.mean(np.log(b))
    import matplotlib.pyplot as plt
    count, bins, ignored = plt.hist(b, 100, density=True, align='mid')
    x = np.linspace(min(bins), max(bins), 10000)
    pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))  \
          / (x * sigma * np.sqrt(2 * np.pi)))
    plt.plot(x, pdf, linewidth=2, color='r')
    plt.axis('tight')
    plt.show()

def fit_to_normal(b,plot = True):
    from scipy.stats import norm
    b = b[b != 0]
    sigma = np.std(b)
    mu = np.mean(b)
    if(plot):
        import matplotlib.pyplot as plt
        count, bins, ignored = plt.hist(b, 100, density=True, align='mid')
        x = np.linspace(min(bins), max(bins), 10000)
        pdf = norm.pdf(x, mu, sigma)
        plt.plot(x, pdf, linewidth=2, color='r')
        plt.axis('tight')
        plt.show()
    print(mu,sigma,b[-1]-b[0])

def fit_linear(x,y):
    from scipy import stats
    x = x[y != 0]
    y = y[y != 0]
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    # print(slope, intercept, r_value, p_value, std_err,y[-1]-y[0])
    return np.array([[slope, intercept, r_value, p_value, std_err,y[-1]-y[0]]])

def filter_data(samples):
    return samples

url = 'https://tickdata.fxcorporate.com/'  ##This is the base url
url_suffix = '.csv.gz'  ##Extension of the file name
symbol = 'EURUSD'  ##symbol we want to get tick data for
FXFolderpath = r'data/fx'

a = get_timedeltaData(my_data, '2018-01-01 23:00:28.378', -1000 * 60 * 60)
b = get_timedeltaData(my_data, '2018-01-01 23:00:28.378', 1000 * 60 * 10)
print(a)
print(b.DateTime.iloc[-1])
(a, b) = prepare_trainData("GBPUSD", "pd,1S")
aupdate = numpy_fillna(a)
npx_data = np.asarray(aupdate)
bupdate = numpy_fillna(b)
npy_data = np.asarray(bupdate)


import matplotlib.pyplot as plt
bb = dataLogReturn(npy_data)
print(bb[0,:,1])
[a1,a2,a3] = bb.shape
for i in range(a1):
    # fit_to_normal(npy_data[i,:,1],False)
    if i == 0:
        y_array = fit_linear(npy_data[i,:,0],(npy_data[i,:,1]+npy_data[i,:,2])/2)
    else:
        y_array = np.vstack((y_array, fit_linear(npy_data[i,:,0],(npy_data[i,:,1]+npy_data[i,:,2])/2)))

def dataNormalization(data):
    # here I try to normalize all the data input
    return data



