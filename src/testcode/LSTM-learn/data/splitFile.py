import sys
import csv
sys.path.insert(0, "src/testcode/LSTM-Neural-Network-for-Time-Series-Prediction-master/")
currentpath = r"src/testcode/LSTM-Neural-Network-for-Time-Series-Prediction-master/"

f = open(currentpath + "/data/testGBPUSD.csv","w+")

with open(currentpath + "/data/GBPUSD.csv") as myfile:
    head = [next(myfile) for x in range(100)]

for i in range(len(head)):
    f.write(head[i])

f.close()
