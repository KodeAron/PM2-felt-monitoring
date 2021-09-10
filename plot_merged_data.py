# -*- coding: utf-8 -*- python3
""" Plot data from various sources

Merge and plot dataframes of 
accelerometer, felt, process, operation data.

Created on March 1 2021 10:03
@author: Aron, Luleå University of Technology
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib import gridspec
from matplotlib import ticker
import numpy as np
import scipy.stats as spstats 
import datetime as dt

import generaltools as gtol
import extractombiner as extcom
import protak
import feltdata

def main():
    df_felt = feltdata.load_data()
    df = extcom.combiner(samespeed=True)
    plot_merged_df(df,df_felt)

def plot_merged_df(df, df_felt):
    
    feature = 'kurtosis' # 'rms' 'kurtosis' 'crest factor'
    aggregate = False
    savefig = True
    nodelist = [] # ['P001F','P001D'] ['P302F','P302D']

    fig = plt.figure()
    # set height ratios for subplots
    gs = gridspec.GridSpec(3, 1, height_ratios=[2, 0.2, 0.8]) 

    first_date = df.index[0]
    last_date = df.index[-1]

    # felt replacements
    felt_replacements = sorted(feltdata.\
        replacement_list(df_felt,first_date,last_date))

    ## first subplot
    ax0 = plt.subplot(gs[0])
    linelist = []
    nNodes = len(df[feature].columns)
    
    # prepare for linear regression by converting datetime to ordinal
    df_repl1 = df[(df.index > felt_replacements[0]+dt.timedelta(days=1))\
        & (df.index < felt_replacements[1]-dt.timedelta(days=1))]
    df_repl2 = df[(df.index > felt_replacements[1]+dt.timedelta(days=1))]
        # & (df.index < felt_replacements[2]-dt.timedelta(days=1))]
    ordinal_dt_repl1 = df_repl1.index.map(dt.datetime.toordinal)
    ordinal_dt_repl2 = df_repl2.index.map(dt.datetime.toordinal)

    if aggregate:
        agg_title = 'std '
        line, = ax0.plot(df.index, df[feature].apply(np.std,axis=1),\
            '-', color='r', label=agg_title+feature,picker=True)
    else:
        # i = 0
        if len(nodelist)==0:
            for column in df[feature]:
                ax0.plot(df.index, df[feature,column],'-',\
                    label=column,picker=True,color='r')
        else:
            for column in df[feature]:
                if column in nodelist:
                    # plot feature for one node (column)
                    ax0.plot(df.index, df[feature,column],'-',\
                        label=column,picker=True)
                    # linear regression
                    LinregressResult = spstats.linregress(\
                        ordinal_dt_repl1,df_repl1[feature,column])
                    y = LinregressResult.slope * ordinal_dt_repl1\
                        + LinregressResult.intercept
                    ax0.plot(df_repl1.index, y,\
                        linestyle='dotted',color='r')
                    LinregressResult = spstats.linregress(\
                        ordinal_dt_repl2,df_repl2[feature,column])
                    y = LinregressResult.slope * ordinal_dt_repl2\
                        + LinregressResult.intercept
                    ax0.plot(df_repl2.index, y,\
                        linestyle='dotted',color='r')
    if feature == 'kurtosis':
        ylim = [-0.5, 5] # kurtosis
    elif feature == 'rms':
        ylim = [0, 0.2] # rms
    elif feature == 'crest factor':
        ylim = [3, 9] # crest factor
    else:
        print('Unknown feature')
        ylim = [-3, 6]
    ax0.set_ylim(ylim[0],ylim[1])

    ## second subplot
    ax1 = plt.subplot(gs[1], sharex = ax0)
    trimproblem_df = protak.digital_problem_df(reason='Trimproblem',\
        first_date=first_date,last_date=last_date)
    line2, = ax1.plot(trimproblem_df['Date'],\
        trimproblem_df['Trimproblem'],'-', color='b',\
            label='Trimproblem',picker=True)
    # massakladd_df = protak.digital_problem_df(reason='Massakladd',\
    #     first_date=first_date,last_date=last_date)
    # line2, = ax1.plot(massakladd_df['Date'],\
    #     massakladd_df['Massakladd'],'-', color='k',\
    #         label='Massakladd',picker=True)
    
    ## third subplot
    # shared axis X
    ax2 = plt.subplot(gs[2], sharex = ax0)
    line3, = ax2.plot(df.index, df['AverageSpeed'],'-',\
        color='g',label='Avg.speed',picker=True)
    # select format of datetime
    # myFmt = mdates.DateFormatter('%d/%m %H:%M') 
    # plt.ax0.xaxis.set_major_formatter(myFmt)
    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.setp(ax1.get_xticklabels(), visible=False)
    # remove last tick label for the second subplot
    # yticks = ax1.yaxis.get_major_ticks()
    # yticks[-1].label1.set_visible(False)
    ax1.yaxis.set_major_locator(ticker.NullLocator())

    # plot felt replacements
    ax0.vlines(felt_replacements, \
        ylim[0], ylim[1], colors='k', linestyles='solid')
    ax1.vlines(felt_replacements, \
        0, 1, colors='k', linestyles='solid')
    ax2.vlines(felt_replacements, \
        380, 1240, colors='k', linestyles='solid')
    ax2.set_ylim(380,1250)

    # select format of datetime
    myFmt = mdates.DateFormatter('%d-%b') 
    ax1.xaxis.set_major_formatter(myFmt)

    # put legend on first subplot
    if not len(nodelist)==0:
        ax0.legend()#loc='upper left')

    # connect picker
    fig.canvas.callbacks.connect('pick_event', gtol.on_pick)

    # title above plot and in filename
    if aggregate==True: title = agg_title + feature
    else: title = feature
    # ax0.title.set_text(title)

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)
    plt.show()

    # save to pdf
    if savefig:
        if len(nodelist)==0:
            nodes = '14'
        else:
            nodes = ','.join(nodelist)
        savename = title + '_' + nodes + "+trim+speed"
        fig.savefig("../saved_plots/" + savename + ".pdf",\
            bbox_inches='tight')


def doublePlot(df_list, plt1items, plt2items):
    fig = plt.figure()
    # set height ratios for subplots
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
    # the first subplot
    ax0 = plt.subplot(gs[0])

    line0, = ax0.plot(df_list[0].Datetime, df_list[0].RMS,\
        color='b',label='rms')
    line1, = ax0.plot(df_list[0].Datetime, df_list[0].KURT,\
        color='r',label='kurtosis')
    # lines = lineObjs(ax0, plt1)

    # the second subplot
    # shared axis X
    ax1 = plt.subplot(gs[1], sharex = ax0)
    # for robustness, should filter for trimproblem
    ptak_dates = df_list[1].STARTDATE[500:-1] 
    line1, = ax1.plot(ptak_dates, np.ones(len(ptak_dates)),\
        '*',  color='b', label='trimproblem')
    plt.setp(ax0.get_xticklabels(), visible=False)
    # remove last tick label for the second subplot
    yticks = ax1.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)
    
    # set format for datetime (on x axis)
    myFmt = mdates.DateFormatter('%d/%m') 
    ax1.xaxis.set_major_formatter(myFmt)

    ax0.legend()
    ax1.legend()
    plt.show()

if __name__ == '__main__':
    main()