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
    print(df[4])


def readData(filename='../data_protak/ProTAK PM2 Pressektion 201001-210228.xlsx',trimproblem=True):
    # extract operation data from spreadsheet and return as dataframe
    # if trimproblem=true then 
    df = pd.read_excel(filename)

    # multifilter=(df['REASONDESCRIPTION']=='Trimproblem')
        # *(df_component['Korsningkategori']=='Rorlig')\
        # *(df_sameTrend['Befastningskategori']=='Pandrol')\
        # *(df_sameTrend['Sliperkategori']=='Betong')\
        # *(df_sameTrend['Ballastkategori']=='M1')\
    # df_trim = df[multifilter]

    # Trimproblem, Massakladd, Hål. More relevant REASONDESCRIPTION ??
    # df_trim= df.set_index(['REASONDESCRIPTION'],\
        # drop=True).loc['Trimproblem'].copy() 
    # df_trim = df[df.REASONDESCRIPTION.isin(["Trimproblem"])].copy().reset_index()
    df_trim= df.set_index(['REASONDESCRIPTION'],drop=True)\
        .loc['Trimproblem'].reset_index(drop=False,inplace=False)
    df_trim['STARTDATE'] = pd.to_datetime(df_trim['STARTDATE'], format='%d-%m-%Y %H:%M:%S')
    df_trim['ENDDATE'] = pd.to_datetime(df_trim['ENDDATE'], format='%d-%m-%Y %H:%M:%S')
    return df_trim

def plotData():
    pass

if __name__ == '__main__':
    main()