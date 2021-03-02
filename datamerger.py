# -*- coding: utf-8 -*- python3
""" Merge and plot dataframes of accelerometer, felt, process, operation data

Read acceleration data in UFF format. Return dataframe or matrix. Save to csv.

Created on March 1 2021 10:03
@author: Aron, Luleå University of Technology
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib import gridspec
import numpy as np

import observer
import protak

def main():
    # stackOverflowTest()
    df_observer = observer.dataUFF_to_featuresDF(sensorPosition = 'P001F', timePeriod = '201027-210221')
    df_protak = protak.readData()
    print(df_protak.columns)
    # plotVibNLogg(df_observer,df_protak)
    doublePlot([df_observer,df_protak], ['RMS','KURT'],['trimproblem'])#,'massakladd'

def plotVibNLogg(df_observer, df_protak):

    fig = plt.figure()
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

    # the first subplot
    ax0 = plt.subplot(gs[0])
    # log scale for axis Y of the first subplot
    # ax0.set_yscale("log")
    line0, = ax0.plot(df_observer.Datetime, df_observer.RMS, color='r', label="RMS")
    line2, = ax0.plot(df_observer.Datetime, df_observer.Kurtosis, color='g')
    

    # the second subplot
    # shared axis X
    ax1 = plt.subplot(gs[1], sharex = ax0)
    ptak_dates=df_protak.STARTDATE[500:-1]
    line1, = ax1.plot(ptak_dates, np.ones(len(ptak_dates)),'*', color='b')
    # myFmt = mdates.DateFormatter('%d/%m %H:%M') # select format of datetime
    # plt.ax0.xaxis.set_major_formatter(myFmt)
    plt.setp(ax0.get_xticklabels(), visible=False)
    # remove last tick label for the second subplot
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    myFmt = mdates.DateFormatter('%d/%m') # select format of datetime
    ax1.xaxis.set_major_formatter(myFmt)

    # put legend on first subplot
    ax0.legend((line0, line2, line1), ('rms', 'kurtosis','logposts'), loc='upper left')

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)
    plt.show()

def stackOverflowTest():
#     import matplotlib.pyplot as plt
#     import numpy as np
#     from matplotlib import gridspec

    # Simple data to display in various forms
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x ** 2)

    fig = plt.figure()
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

    # the first subplot
    ax0 = plt.subplot(gs[0])
    # log scale for axis Y of the first subplot
    ax0.set_yscale("log")
    line0, = ax0.plot(x, y, color='r')

    # the second subplot
    # shared axis X
    ax1 = plt.subplot(gs[1], sharex = ax0)
    line1, = ax1.plot(x, y, color='b', linestyle='--')
    plt.setp(ax0.get_xticklabels(), visible=False)
    # remove last tick label for the second subplot
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)

    # put legend on first subplot
    ax0.legend((line0, line1), ('red line', 'blue line'), loc='lower left')

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)
    plt.show()

def doublePlot(df_list, plt1items, plt2items):
    # Simple data to display in various forms
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x ** 2)

    fig = plt.figure()
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    # the first subplot
    ax0 = plt.subplot(gs[0])

    line0, = ax0.plot(df_list[0].Datetime, df_list[0].RMS, color='b',label='rms')
    line1, = ax0.plot(df_list[0].Datetime, df_list[0].KURT, color='r',label='kurtosis')
    # lines = lineObjs(ax0, plt1)

    # the second subplot
    # shared axis X
    ax1 = plt.subplot(gs[1], sharex = ax0)
    ptak_dates = df_list[1].STARTDATE[500:-1] # for robustness, should filter for trimproblem
    line1, = ax1.plot(ptak_dates, np.ones(len(ptak_dates)),'*',  color='b', label='trimproblem')
    plt.setp(ax0.get_xticklabels(), visible=False)
    # remove last tick label for the second subplot
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)
    
    # set format for datetime (on x axis)
    myFmt = mdates.DateFormatter('%d/%m') # select format of datetime
    ax1.xaxis.set_major_formatter(myFmt)

    ax0.legend()
    ax1.legend()
    plt.show()

def lineObjs(axis, pltList):
    # return line tuple from axis and list of strings for desires data


    return lines


def plotVibNStops(filename):
    pass
    return # dataframe

def plotVibNLoggNStops():
    pass
    # plots

if __name__ == '__main__':
    main()