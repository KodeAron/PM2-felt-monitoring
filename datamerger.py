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

import generaltools as gtol
import observer
import protak
import feltdata

def main():
    # stackOverflowTest()
    df_observer = observer.load_data(positions = ['P001F'], timeperiod = '201027-210221')
    df_protak = protak.load_data()
    df_felt = feltdata.load_data()
    # print(df_protak.columns)
    plotVibNLogg(df_observer[0]['featuresDF'],df_protak, df_felt)
    # print(df_observer)
    # doublePlot([df_observer,df_protak], ['RMS','KURT'],['trimproblem'])#,'massakladd'

def plotVibNLogg(df_vibsensor, df_protak, df_felt):

    fig = plt.figure()
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 

    # the first subplot
    ax0 = plt.subplot(gs[0])
    # log scale for axis Y of the first subplot
    # ax0.set_yscale("log")
    line0, = ax0.plot(df_vibsensor.Datetime, df_vibsensor.RMS, color='r', label="RMS",picker=True)
    line1, = ax0.plot(df_vibsensor.Datetime, df_vibsensor.KURT, color='g', label="kurtosis",picker=True)

    # felt replacements
    ax0.vlines(df_felt.INSTALLED, -10, 10, colors='k', linestyles='solid', label='replacements')

    # the second subplot
    # shared axis X
    ax1 = plt.subplot(gs[1], sharex = ax0)
    ptak_dates=df_protak.STARTDATE[500:-1]
    line2, = ax1.plot(ptak_dates, np.ones(len(ptak_dates)),'*', color='b',label='trimproblem',picker=True)
    # myFmt = mdates.DateFormatter('%d/%m %H:%M') # select format of datetime
    # plt.ax0.xaxis.set_major_formatter(myFmt)
    plt.setp(ax0.get_xticklabels(), visible=False)
    # remove last tick label for the second subplot
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    
    myFmt = mdates.DateFormatter('%d/%m') # select format of datetime
    ax1.xaxis.set_major_formatter(myFmt)

    # put legend on first subplot
    ax0.legend((line0, line1, line2), (line0.get_label(), line1.get_label(),'trimproblem'),loc='upper left') #

    # connect picker
    fig.canvas.callbacks.connect('pick_event', gtol.on_pick)

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)
    plt.show()

def doublePlot(df_list, plt1items, plt2items):
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