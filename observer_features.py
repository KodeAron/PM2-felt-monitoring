# -*- coding: utf-8 -*- python3
""" Calculate features for each 

Created on Mar 26 2021 08:20
@author: Aron, Luleå University of Technology
"""
import pandas as pd
import observer_merge as obsm
import numpy as np
import scipy.stats as spstats 
import datetime as dt

picklefilepath = obsm.picklefilepath # retrieve file location from observer_merge.py

def main():
    features()

def features():
    # calculate features for each node and strip non-interesting columns,
    # delete (a)larm measurements (StorageReason=1)
    # and group by date
    measdf = pd.read_pickle(picklefilepath)
    # print(measdf.columns)
    # print(measdf.index)

    df = measdf[['MeasDate','IDNode','NodeName','StorageReason','Speed','MeasValue','RawData']].copy()

    # print(df[df['NodeName']=='P303D'].head()) # to check if StorageReason=1 really is larm, seems so'

    # delete larm measurements, i.e. only keep sccheduled (StorageReason=0)
    df = df[df['StorageReason'] == '0'] #.reset_index(drop=True,inplace=False)
        #.sort_values(by=['MeasDate','IDNode'])

    # remove dates before 2020-11-04
    df = df[df['MeasDate'] > dt.datetime(2020,11,4)].reset_index(drop=True,inplace=False)
    
    # check for missing data
    if df[df['RawData'].isnull()].empty:
        print('No missing raw data.')
    else:
        print('Missing data')
        print(df[df['RawData'].isnull()])

    # calculate rms and kurtosis and add result in new columns
    df['rms'] = df['RawData'].apply(vec_rms)
    df['kurtosis'] = df['RawData'].apply(vec_kurtosis)

    # # print measurements that belongs together
    # print(df[df['MeasDate'].dt.floor(freq = 'D') == dt.datetime(2020,11,4)])

    # group measurements that were performed close in time
    df.set_index('MeasDate').groupby(pd.Grouper(freq='H'))
    print(df)

def vec_rms(data_array):
    val_rms = np.sqrt(np.mean(data_array**2))
    return val_rms

def vec_kurtosis(data_array):
    val_kurtosis = spstats.kurtosis(np.abs(data_array))
    return val_kurtosis

if __name__ == '__main__':
    main()