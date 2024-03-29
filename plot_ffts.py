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
picklefilepath = '../data_observer/pickles/' + \
    '1aPressT_Acc_ej-nyp_201015-210325'
import feltdata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
import generaltools as gtol

# load raw vibration data 
measdf = pd.read_pickle(picklefilepath)
# print(measdf.columns)

# create a copy (df) with only relevant columns
df = measdf[['MeasDate','IDNode','NodeName','StorageReason','Speed',\
    'MeasValue','SampleRate','TimesignalPulses',\
        'SpectraLines','RawData']].copy()

# delete larm measurements, i.e. only keep sccheduled (StorageReason=0)
df = df[df['StorageReason'] == '0'].drop(labels='StorageReason',\
    axis=1,inplace=False)

# select, and filter, one node
nodename = 'P301F'
df = df[df['NodeName'] == nodename]

# choose whether to normalise on com
cpm_norm = False

# select time interval and remove other measurements
felt_df = feltdata.load_data()
felt_replacements = feltdata.replacement_list(felt_df,\
    first_date=df.iloc[0].MeasDate,last_date=df.iloc[-1].MeasDate)
# for 201015-210325 this will return two dates, i.e. two replacements
# return measurements between these two dates
df = df[(df['MeasDate'] > felt_replacements[1]) & \
    (df['MeasDate'] < felt_replacements[0])]\
        .reset_index(drop=True,inplace=False)

print(df[['MeasDate','Speed']])

# select samples
samples = [df.iloc[4], df.iloc[-3]]
# colors = ['g','r']
# # create figure
fig = plt.figure(figsize=(8,4))
for sample in samples:
    measdate_str = str(sample.MeasDate)
    speed = float(sample.Speed)
    speed_str = str(round(speed,1))
    label = measdate_str + ', cpm=' + speed_str
    print(label)
    # run fft
    samplerate = float(sample.SampleRate)
    print('samplerate',samplerate)
    # N = float(sample.SpectraLines)
    N = len(sample.RawData)
    # print('N =',N)
    duration = N/samplerate
    print('duration =',duration)
    # N = samplerate * DURATION

    yf = rfft(sample.RawData)
    xf = rfftfreq(N, 1 / samplerate) #/float(sample.Speed)
    if cpm_norm:
        xf = xf/(speed/60)

    abs_yf = np.abs(yf)
    plt.plot(xf, abs_yf, label=label,linewidth=0.2,picker=True)

    # plot the lower end of the spectrum
    if cpm_norm:
        cutoff_low = 0
        cutoff_high = 500/(speed/60)
    else:
        cutoff_low = 0
        cutoff_high = 500
    index_cutoff_low = sum(xf<cutoff_low)
    index_cutoff_high = sum(xf<cutoff_high)
    # amplitude_cutoff = max(abs_yf[index_cutoff_low:index_cutoff_high])/2

    plt.xlim(cutoff_low,cutoff_high)
    # plt.ylim(0,amplitude_cutoff)
    plt.ylim(0,100)

# connect picker
fig.canvas.callbacks.connect('pick_event', gtol.on_pick)
# plot
# plt.gca().set_yscale('log')

if cpm_norm:
    freq_norm = 'cpmnorm_'
    plt.gca().set_xlabel("Frequency / Machine speed [Hz/Hz]")
else:
    freq_norm = ''
    plt.gca().set_xlabel("Frequency [Hz]")
    
# plt.title(nodename)
plt.legend()
plt.show()

savename = nodename + "_Sp_" + freq_norm + str(round(cutoff_low,1)) + \
    '-' + str(round(cutoff_high,1)) + "_" + \
    "_".join([sample.MeasDate.strftime("%y%m%d") for sample in samples])
# print(savename)
fig.savefig("../saved_plots/" + savename + ".pdf", bbox_inches='tight')


# ## calculate and plot mean freq

# meanfreq = []

# # loop through the df filtered out earlier, for node and interval
# for index in range(len(df)):
#     # run fft
#     samplerate = float(sample.SampleRate)
#     N = len(sample.RawData)
#     # duration = N/samplerate

#     yf = rfft(sample.RawData)
#     xf = rfftfreq(N, 1 / samplerate)
#     abs_yf = np.abs(yf)
#     meanfreq.append(np.average(xf, weights=abs_yf))

# plt.plot(meanfreq)
# plt.show()