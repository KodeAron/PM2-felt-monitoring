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


def load_data(filename=fullpath_data):
    # extract felt data from spreadsheet and return as dataframe
    df = pd.read_excel(filename)
    return df

if __name__ == '__main__':
    main()