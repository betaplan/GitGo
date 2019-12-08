#This is the toolbox
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

class Dataplot():
    """A class for loading and transforming data for the lstm model"""

    def __init__(self, filename, split, cols, dataformat="", dtc = ""):
        dataframe = pd.read_csv(filename)
        if(dtc == ""):
            dateTimeCol = 'DateTime'
        else:
            dateTimeCol = dtc
        try:
            if( dataformat == ""):
                dataframe[dateTimeCol] = pd.to_datetime(dataframe[dateTimeCol])
                dataframe = self.datetime_array_to_float(dataframe)
            else:
                dataframe[dateTimeCol] = pd.to_datetime(dataframe[dateTimeCol],format = dataformat)
                dataframe = self.datetime_array_to_float(dataframe)
        except:
            print("No 'DateTime'")
        i_split = int(len(dataframe) * split)
        self.data_train = dataframe.get(cols).values[:i_split]
        self.data_test  = dataframe.get(cols).values[i_split:]
        self.len_train  = len(self.data_train)
        self.len_test   = len(self.data_test)
        self.len_train_windows = None

    def plot(self, dataplotx,dataploty):
        plt.plot(dataplotx,dataploty)
        plt.ylabel('')
        plt.show()

    def float_to_datetime(fl):
        return datetime.datetime.fromtimestamp(fl)

    def datetime_to_float(d):
        return d.timestamp()

    def datetime_array_to_float(self, data):
        epoch = datetime.datetime(1970, 1, 1)
        col_value = data.columns.values
        dataout = data.to_numpy()
        dataout.transpose((1, 0))[0] = [(d - epoch).total_seconds() for d in dataout.transpose((1, 0))[0]]
        return pd.DataFrame(dataout).set_axis(col_value, axis='columns', inplace=False)

    def get_bars(symbol):
        data = api.get_barset(symbol, 'day', limit = 1000)
        data = data.df[symbol]['close']
        return data

    def correlation(equity_list):

        df = pd.DataFrame()
        equity_columns = []

        # Get symbol history
        for symbol in equity_list:
            try:
                symbol_df = get_bars(symbol)
                df = pd.concat([df, symbol_df], axis=1)
                equity_columns.append(symbol)
            except:
                print('Exception with {}'.format(symbol))

        df.columns = equity_columns

        # Get correlation and sort by sum
        sum_corr = df.corr().sum().sort_values(ascending=True).index.values

        return df[sum_corr].corr()