import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sb

np.seterr(divide='ignore', invalid='ignore')

# Quick way to test just a few column features
# stocks = pd.read_csv('supercolumns-elements-nasdaq-nyse-otcbb-general-UPDATE-2017-03-01.csv', usecols=range(1,16))

stocks = pd.read_csv('test.csv')

print(stocks.head())

str_list = []
for colname, colvalue in stocks.iteritems():
    if type(colvalue[1]) == str:
         str_list.append(colname)

# Get to the numeric columns by inversion
num_list = stocks.columns.difference(str_list)

stocks_num = stocks[num_list]

print(stocks_num.head())

stocks_num = stocks_num.fillna(value=0, axis=1)

X = stocks_num.values

from sklearn.preprocessing import StandardScaler
X_std = StandardScaler().fit_transform(X)

f, ax = plt.subplots(figsize=(12, 10))
plt.title('Pearson Correlation of Concept Features (Elements & Minerals)')

# Draw the heatmap using seaborn
sb.heatmap(stocks_num.astype(float).corr(),linewidths=0.25,vmax=1.0, square=True, cmap="YlGnBu", linecolor='black', annot=True)
sb.plt.show()

from sklearn.decomposition import PCA
import numpy as np
pca = PCA()
pca.fit(X)
print(pca.components_)