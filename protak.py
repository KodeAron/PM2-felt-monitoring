# -*- coding: utf-8 -*- python3
""" protak data reader

Created on Feb 25 2021 10:10
@author: Aron, Luleå University of Technology
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

def main():
    filename = '../data_protak/ProTAK PM2 Pressektion 201001-210228.xlsx'
    df = load_data()
    # print(df[df.REASONDESCRIPTION=='Trimproblem'])
    boolean_date_plot(df)


def load_data(filename='../data_protak/ProTAK PM2 Pressektion 201001-210228.xlsx',
    reasonfilter=['Trimproblem']):
    
    # read operation data from spreadsheet and return as dataframe
    df = pd.read_excel(filename)
    # create new df fitlered on REASONDESCRIPTION in reasonfilter
    # Trimproblem, Massakladd, Hål. More relevant REASONDESCRIPTION ??
    df_trim = df[df.REASONDESCRIPTION.isin(reasonfilter)].copy().reset_index(drop=True,inplace=False)
    # remove empty columns
    df_trim.dropna(axis=1, how='all', inplace=True) 
    # convert to datetime format
    df_trim['STARTDATE'] = pd.to_datetime(df_trim['STARTDATE'], format='%d-%m-%Y %H:%M:%S')
    df_trim['ENDDATE'] = pd.to_datetime(df_trim['ENDDATE'], format='%d-%m-%Y %H:%M:%S')
    return df_trim
    
def boolean_date_plot(dataframe):
    # df_trim= dataframe.set_index(['REASONDESCRIPTION'],\
    #     drop=True).loc['Trimproblem'].copy() 
    plt.plot(dataframe.STARTDATE, np.ones(len(dataframe.STARTDATE)),'*', label="")
    myFmt = mdates.DateFormatter('%d/%m %H:%M') # select format of datetime
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.show()

# def plotData(dataframe):
#     pass

def check_datetime_for_problem(dataframe,datetime):
    # check if specific point in time had any problem
    # return boolean value and REASONDESCRIPTION

    return problem_bool, reasondescription

if __name__ == '__main__':
    main()