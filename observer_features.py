# -*- coding: utf-8 -*- python3
""" Calculate features for each 

Created on Mar 26 2021 08:20
@author: Aron, Luleå University of Technology
"""
import pandas as pd
import observer_merge as obsm
import numpy as np
import scipy.stats as spstats 

picklefilepath = obsm.picklefilepath # retrieve file location from observer_merge.py

def main():
    features()

def features():
    # calculate features for each node and strip non-interesting columns,
    # delete (a)larm measurements (StorageReason=1)
    # and group by date
    measdf = pd.read_pickle(picklefilepath)

    print(measdf.columns)
    print(measdf.index)

    df = measdf[['MeasDate','IDNode','NodeName','StorageReason','Speed','MeasValue','RawData']].copy()

    print(df[df['NodeName']=='P303D'].head()) # to check if StorageReason=1 really is larm, seems so'

    df['rms'] = df['RawData'].apply(vec_rms)
    df['kurtosis'] = df['RawData'].apply(vec_kurtosis)

def vec_rms(data_array):
    val_rms = np.sqrt(np.mean(data_array**2))
    return val_rms

def vec_kurtosis(data_array):
    val_kurtosis = spstats.kurtosis(np.abs(data_array))
    return val_kurtosis

if __name__ == '__main__':
    main()