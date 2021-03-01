# -*- coding: utf-8 -*- python3
""" protak data reader

Created on Feb 25 2021 10:10
@author: Aron, Luleå University of Technology
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def main():
    filename = '../data_protak/ProTAK PM2 Pressektion 201001-210228.xlsx'
    df = readData()
    print(df)


def readData(filename='../data_protak/ProTAK PM2 Pressektion 201001-210228.xlsx',trimproblem=True):
    # extract operation data from spreadsheet and return as dataframe
    df = pd.read_excel(filename)
    return df

def plotData():
    pass

if __name__ == '__main__':
    main()