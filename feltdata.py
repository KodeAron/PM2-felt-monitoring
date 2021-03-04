# -*- coding: utf-8 -*- python3
""" Felt data reader

Created on Feb 25 2021 11:30
@author: Aron, Luleå University of Technology
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

path_data = '../data_felt/'
filename_data = 'Press1T_felt_log.xlsx'
fullpath_data = path_data + filename_data

def main():
    df = load_data()
    print(df.columns)
    print(df)
    plot_feltchange(df)

def load_data(filename=fullpath_data,recalculate_runtime=True):
# extract felt data from spreadsheet and return as dataframe
    df = pd.read_excel(filename)
    # df.convert_dtypes()
    df['INSTALLED'] = pd.to_datetime(df['INSTALLED']) #, format='%Y-%m-%d')
    df['REMOVED'] = pd.to_datetime(df['REMOVED'])
    if recalculate_runtime:
        df['RUNTIME']=df['REMOVED']-df['INSTALLED']
    return df

def plot_feltchange(feltDF):
# plot dates where the felt was changed
    plt.vlines(feltDF.INSTALLED, -5, 5, colors='k', linestyles='solid', label='replacements')
    plt.show()

if __name__ == '__main__':
    main()