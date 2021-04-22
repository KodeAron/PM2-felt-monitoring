# -*- coding: utf-8 -*- python3
""" Extract, calculate features and combine data into one dataframe

Observer data: calculate features and restructre so that measurements 
performed close in time are grouped together. Sorted on first MeasDate for each group.

Created on Mar 26 2021 08:20
@author: Aron, Luleå University of Technology
"""
import pandas as pd
import numpy as np
import scipy.stats as spstats 
import datetime as dt

import observer_merge as obsm
import protak
import feltdata

picklefilepath = obsm.picklefilepath # retrieve file location from observer_merge.py

def main():
    # features()
    df = combiner()
    print(df)

def combiner(samespeed=False):
    # get df from observer data
    df = features(samespeed)
    # add column with bool values for Trimproblem
    df['Trimproblem'] = df.LastMeasDate.apply(protak.check_datetime_for_Trimproblem)
    df['Massakladd'] = df.LastMeasDate.apply(protak.check_datetime_for_Massakladd)
    df['Hal'] = df.LastMeasDate.apply(protak.check_datetime_for_Hal)
    return df

def features(samespeed=False):
    # calculate features for each node and strip non-interesting columns,
    # delete (a)larm measurements (StorageReason=1)
    # and group by date
    measdf = pd.read_pickle(picklefilepath)
    # print(measdf.columns)
    # print(measdf.index)

    df = measdf[['MeasDate','IDNode','NodeName','StorageReason','Speed','MeasValue','RawData']].copy()

    # print(df[df['NodeName']=='P303D'].head()) # to check if StorageReason=1 really is larm, seems so'

    # delete larm measurements, i.e. only keep sccheduled (StorageReason=0)
    df = df[df['StorageReason'] == '0'].drop(labels='StorageReason',axis=1,inplace=False) #.reset_index(drop=True,inplace=False)
        #.sort_values(by=['MeasDate','IDNode'])

    # remove dates before 2020-11-04
    df = df[df['MeasDate'] > dt.datetime(2020,11,4)].reset_index(drop=True,inplace=False)
    
    # check for missing data
    if df[df['RawData'].isnull()].empty:
        # print('No missing raw data.')
        pass
    else:
        print('Missing data')
        print(df[df['RawData'].isnull()])

    # calculate features and add result in new columns
    df['rms'] = df['RawData'].apply(vec_rms)
    df['kurtosis'] = df['RawData'].apply(vec_kurtosis)
    df['crest factor'] = df['RawData'].apply(vec_crest)

    # # print measurements that belongs together
    # print(df[df['MeasDate'].dt.floor(freq = 'D') == dt.datetime(2020,11,4)])

    # add column where datetime is floored to hour to simplify grouping/combining
    df['MeasHour'] = df['MeasDate'].dt.floor(freq='H')

    # drop some columns
    df = df.drop(labels=['MeasValue','RawData','IDNode'],axis=1,inplace=False)

    # reshape dataframe
    df_unstack = df.set_index(['MeasHour','NodeName']).unstack(level=-1)

    if samespeed:
        # warning if speed std is too big
        speed_std_threshold = 20
        speed_std = df_unstack.Speed.astype(float).std(axis=1) > speed_std_threshold
        if speed_std.any():
            print('Speed std > ',str(speed_std_threshold))
            print(df_unstack[speed_std].Speed)
            # drop the rows where the std of speed exceeds the threshold
            df_unstack = df_unstack[speed_std==0]

    # calculate average speed and add in column
    df_unstack['AverageSpeed'] = df_unstack.Speed.astype(float).mean(axis=1)
    # drop speed column
    df_unstack.drop(labels=['Speed'],axis=1,inplace=True)

    # replace index with first MeasDate, i.e. minimum date for each row
    mindate = df_unstack.MeasDate.min(axis=1)
    df_unstack = df_unstack.set_index(mindate)

    # add last MeasDate
    df_unstack['LastMeasDate'] = df_unstack.MeasDate.max(axis=1)
    # add difference between first and last MeasDate. dt.seconds converts it to seconds
    df_unstack['DiffMeasDate'] = (df_unstack.MeasDate.max(axis=1)-df_unstack.MeasDate.min(axis=1)).dt.seconds

    # drop MeasDate column
    df_unstack.drop(labels=['MeasDate'],axis=1,inplace=True)

    return df_unstack

def vec_rms(data_array):
    val_rms = np.sqrt(np.mean(data_array**2))
    return val_rms

def vec_kurtosis(data_array):
    val_kurtosis = spstats.kurtosis(np.abs(data_array))
    return val_kurtosis

def vec_crest(data_array):
    val_crest = max(np.abs(data_array))/vec_rms(data_array)
    return val_crest

if __name__ == '__main__':
    main()