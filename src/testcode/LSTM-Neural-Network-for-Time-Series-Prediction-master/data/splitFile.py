import sys
import pandas as pd
sys.path.insert(0, "src/testcode/LSTM-Neural-Network-for-Time-Series-Prediction-master/")
currentpath = r"src/testcode/LSTM-Neural-Network-for-Time-Series-Prediction-master/"



user_view_db = pd.read_table(currentpath + "/data/GBPUSD.csv",sep=',',chunksize=1000000)
for chunk in user_view_db:
    a = chunk
    break

# df = pd.concat([chunk for chunk in user_view_db],ignore_index=True)

a.set_index('DateTime') 
a['Close'] = a['closeBid']
a['Delta'] = a['closeBid'] - a['closeAsk']
a.loc[a.Delta == 0, 'Delta'] = 0.00001
a = a[['DateTime','Close', 'Delta']]

a['DateTime'] = pd.to_datetime(a.DateTime)
a['DateTime'] = pd.to_numeric(a['DateTime'])
a.to_csv(currentpath + "/data/testGBPUSD.csv", index=False)