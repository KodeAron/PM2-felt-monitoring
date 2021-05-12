# -*- coding: utf-8 -*- python3

picklefilepath = '../data_observer/pickles/' + '1aPressT_Acc_ej-nyp_201015-210325'
import generaltools as gtol
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

def main():
    measdf = pd.read_pickle(picklefilepath)
    # dates for P001F
    # date = dt.datetime(2021,1,1,7) # high kurtosis (4.65)
    date = dt.datetime(2020,12,25,14) # low kurtosis (-0.030)
    plot_timesignal(measdf,'P001F',date,True)

def plot_timesignal(measdf,nodename,date,savefig=False):
    # load raw vibration data 
    # print(measdf.columns)

    fig = plt.figure()#figsize=(8,4))

    # create a copy (df) with only relevant columns
    # df = measdf[['MeasDate','IDNode','NodeName','StorageReason','Speed',\
    #     'MeasValue','SampleRate','TimesignalPulses','SpectraLines','RawData']].copy()
    df = measdf[['MeasDate','IDNode','NodeName','StorageReason','Speed',\
        'MeasValue','SampleRate','TimesignalPulses','TimesignalLines','RawData']].copy()

    # delete larm measurements, i.e. only keep scheduled (StorageReason=0)
    df = df[df['StorageReason'] == '0'].drop(labels='StorageReason',axis=1,inplace=False)

    # select, and filter, one node
    df = df[df['NodeName'] == nodename]

    
    print(df.head())
    print(df['SampleRate'].head())

    date_selection,date_error = gtol.nearest(df.MeasDate,date)
    print('date_selection = ',date_selection)
    print('date_error = ',date_error)

    signal = df[df['MeasDate'] == date_selection].iloc[0]

    samplerate = float(signal.SampleRate)
    nSamples = int(signal.TimesignalLines)

    measurement_time = nSamples/samplerate
    x = np.linspace(0,measurement_time,nSamples)

    y = signal.RawData

    # plt.plot(x, y, linewidth=0.2,picker=True)
    plt.plot(x, y, linewidth=0.8,picker=True)

    plt.xlim(1,1.2)
    # plt.gca().autoscale()
    # plt.ylim()

    # connect picker
    fig.canvas.callbacks.connect('pick_event', gtol.on_pick)
    
    title = nodename + " Acceleration " + signal.MeasDate.strftime("%Y-%m-%d %H:%M")
    plt.title(title)
    plt.gca().set_xlabel('time [s]')
    # plt.legend()
    plt.show()

    if savefig:
        savename = nodename + "_Acc_" + signal.MeasDate.strftime("%y%m%d") + '_snip_1-1.2'
        # print(savename)
        fig.savefig("../saved_plots/" + savename + ".pdf", bbox_inches='tight')

if __name__ == '__main__':
    main()