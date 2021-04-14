# -*- coding: utf-8 -*- python3
""" plot acceleration spectrums

Load the raw acceleration data, filter for desired node, 
calculate ffts and plot. 

Created on Apr 2021 15:40
@author: Aron, Luleå University of Technology
"""
# import observer_merge as obsm
# picklefilepath = obsm.picklefilepath
# or just hard code it for increased speed
picklefilepath = '../data_observer/pickles/' + '1aPressT_Acc_ej-nyp_201015-210325'
import pandas as pd

# load raw vibration data 
measdf = pd.read_pickle(picklefilepath)
print(measdf.columns)

# create a copy (df) with only relevant columns
df = measdf[['MeasDate','IDNode','NodeName','StorageReason','Speed',\
    'MeasValue','SampleRate','TimesignalPulses','SpectraLines','RawData']].copy()

# delete larm measurements, i.e. only keep sccheduled (StorageReason=0)
df = df[df['StorageReason'] == '0'].drop(labels='StorageReason',axis=1,inplace=False)

# select, and filter, one node
nodename = 'P301F'
df = df[df['NodeName'] == nodename]

# select time interval and remove other measurements
import feltdata
felt_df = feltdata.load_data()
felt_replacements = feltdata.replacement_list(felt_df,\
    first_date=df.iloc[0].MeasDate,last_date=df.iloc[-1].MeasDate)
# for 201015-210325 this will return two dates, i.e. two replacements
# return measurements between these two dates
df = df[(df['MeasDate'] > felt_replacements[1]) & (df['MeasDate'] < felt_replacements[0])].reset_index(drop=True,inplace=False)

print(df.head())

# select a sample
sample = df.iloc[0]

# run fft
from scipy.fft import rfft, rfftfreq
samplerate = float(sample.SampleRate)
# N = float(sample.SpectraLines)
N = len(sample.RawData)
print(N)
duration = N/samplerate
print('duration =',duration)
# N = samplerate * DURATION

yf = rfft(sample.RawData)
xf = rfftfreq(N, 1 / samplerate)

# plot
import numpy as np
import matplotlib.pyplot as plt
plt.plot(xf, np.abs(yf))
plt.show()