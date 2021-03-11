# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 09:37:40 2018

@author: lt54159
"""

import numpy as np
import pandas as pd
path = r'I:\Linan\self\a.csv'

class tsdata():
    def __init__(self, *args):
        self.colNames = []
        self.dataFrames = []
        self.colId = []
        self.input_dataRN = []

    def importData(self, *args):
        arg = args[0]
        if (type(arg) == str ):
            try:
                input_data = pd.read_csv(arg)
            except UnicodeDecodeError:
                try:
                    input_data = pd.read_csv(arg, encoding="gbk", index_col=False)
                except UnboundLocalError:
                    print('Input str not a valid path')
        if(isinstance(arg, pd.DataFrame)):
            input_data = arg
        if (type(arg)==list):
            input_data = arg
        input_data = input_data.rename(columns={'date': 'DateTime','Date': 'DateTime','DATE': 'DateTime','日期': 'DateTime',
        'Time': 'DateTime', 'time': 'DateTime', '时间': 'DateTime', 'TIME': 'DateTime'})
        try:
            input_data['DateTime'] = pd.to_datetime(input_data['DateTime'], format="%Y/%m/%d")
        except:
            try:
                input_data['DateTime'] = pd.to_datetime(input_data['DateTime'], format="%d/%m/%Y")
            except:
                try:
                    input_data['DateTime'] = pd.to_datetime(input_data['DateTime'], format="%m/%d/%Y")
                except:
                    try:
                        input_data['DateTime'] = pd.to_datetime(input_data['DateTime'], format="%Y-%m-%d")
                    except:
                        print('unknown date format')
        self.input_dataRN = input_data.set_index('DateTime')
        self.input_dataRN = self.input_dataRN.loc[~self.input_dataRN.index.duplicated(keep='first')]

    def insetData(self, asset, *args):
        self.colId.append(asset)
        dfdata = self.importData(args[0])
        newColName = list(self.input_dataRN.columns.values)
        try:
            self.colNames = list(set(self.colNames.append(newColName)))
        except:
            self.colNames = newColName
        if(len(list(self.input_dataRN.columns.values))>0):
            newListIndex = 0
            for index, col in enumerate(newColName):
                selfIndex = self.colNames.index(col)
                try:
                    # self.dataFrames[selfIndex] = \
                    #     self.dataFrames[selfIndex].loc[~self.dataFrames[selfIndex].index.duplicated(keep='first')]
                    self.dataFrames[selfIndex] = pd.concat([self.dataFrames[selfIndex], self.input_dataRN.loc[:,col]],
                     ignore_index=False, axis=1)
                    if(self.dataFrames[selfIndex].columns.values[0]!=self.colId[0]):
                        self.dataFrames[selfIndex] = self.dataFrames[selfIndex].rename(
                            columns={self.dataFrames[selfIndex].columns.values[0]: self.colId[0]})
                    # print(selfIndex,self.dataFrames[selfIndex].head())
                except ValueError:
                    # print(selfIndex, self.input_dataRN.loc[:, col])
                    self.dataFrames[selfIndex] = self.input_dataRN.loc[:, col]
                except IndexError:
                    # print(self.input_dataRN[col])
                    self.dataFrames.append(self.input_dataRN.loc[:, col])
                # except pd.core.indexes.base.InvalidIndexError:
                #     print("InvalidIndexError")
                #     pass
                    # print("pd.core.indexes.base.InvalidIndexError: ", self.input_dataRN.loc[:, col])
                    # self.dataFrames.append(self.input_dataRN.loc[:, col])

                self.dataFrames[selfIndex] = self.dataFrames[selfIndex].rename(columns={'0': self.colId[0], self.colNames[selfIndex]: asset})
        else:
            print(args," have no data!")

        return 0

    def find(self, *args):
        find_list = args[0]
        if(type(find_list) == str):
            return self.find_element(find_list)
        elif(type(find_list) == list):
            print()
            return [self.find_element(find_element)
                      for find_element in find_list]
        else:
            print("Unknown data type")

    def find_element(self, name):
        if (name in self.colNames):
            return self.colNames.index(name)
        else:
            print(name + " not in list")

    def correlation(self, *args):
        return 0
    
    def cal_vol(inputmatrix, model,returns = "lg",a = 0.1, b = 0.87, VL = 0.01):
        if (returns == "pc"):
            return_matirx = inputmatrix.pct_change()
        if (returns == "lg"):
            return_matirx = np.log(inputmatrix) - np.log(inputmatrix.shift(1))
        return_matirx = np.array(return_matirx[np.isfinite(return_matirx)])
        print(model)
        if(model == "normal"):
            average = np.mean(return_matirx)
            vol_sqr = 0.0
            for x in range(return_matirx.size):            
                vol_sqr = (return_matirx[x] - average)**2
            vol_sqr /= inputmatrix.size()
            return (vol_sqr)**0.5
        if(model == "ewma"):
            vol_sqr = 0.0
            for x in range(return_matirx.size):            
                vol_sqr = (1-a)*vol_sqr + (a)* (return_matirx[x])**2
            return (vol_sqr)**0.5
        if(model == "garch11"):
            vol_sqr = 0.0
            if (a+b>1):
                print("a+b>1")
                return 0.0
            for x in range(return_matirx.size):
                vol_sqr = (1-a-b)*VL + a * (return_matirx[x])**2 + b * vol_sqr
            return (vol_sqr)**0.5

# testdata = tsdata(path)
# testdata.input_dataRN
                    
def CheckPSD(tmp):
    #We Check if the matrix is semi-positive-definite
    eigVec=np.linalg.eigvalsh(tmp)
    nn = tmp.shape[0]
    PSD = np.all(eigVec > 0.01)
    minEig = np.min(eigVec)
    maxEig = np.max(eigVec)
    PosEig = np.sum(eigVec > 0.01) 
    minPosEig = np.min(eigVec[eigVec>0])
    return PSD, minEig, maxEig, (nn-PosEig), minPosEig
       
def GetNearPSD(tmp,epsilon):
    eigval, eigvec = np.linalg.eigh(tmp)
    Q = np.float64(eigvec)
    eigval = np.abs(eigval)
    xdiag = np.float64(np.diag(np.maximum(eigval, epsilon)))
    res = np.dot(Q,np.dot(xdiag,Q.T))
    res = 0.5*(res + res.T)
    ## For some numerical issues sometimes needs to be ran twice
    eigval, eigvec = np.linalg.eigh(res)
    Q = np.float64(eigvec)
    eigval = np.abs(eigval)
    xdiag = np.float64(np.diag(np.maximum(eigval, epsilon)))
    res = np.dot(Q,np.dot(xdiag,Q.T))
    res = 0.5*(res + res.T) 
    return res
            
        