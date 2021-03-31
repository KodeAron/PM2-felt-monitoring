# -*- coding: utf-8 -*- python3
""" protak data reader

Created on Feb 25 2021 10:10
@author: Aron, Luleå University of Technology
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

protakfilepath = '../data_protak/ProTAK statistics raw PM2 2020-10-30 - 2021-03-26.xlsx'

def main():
    # filename = '../data_protak/ProTAK PM2 Pressektion 201001-210228.xlsx'
    df = load_data()
    # print(df[df.Reason=='Trimproblem'])
    boolean_date_plot(df)


def load_data(filename=protakfilepath,
    reasonfilter=['Trimproblem']):
    
    # read operation data from spreadsheet and return as dataframe
    df = pd.read_excel(filename,header=6)
    # create new df fitlered on Reason in reasonfilter
    # Trimproblem, Massakladd, Hål. More relevant Reason ??
    df = df[df.Reason.isin(reasonfilter)].reset_index(drop=True,inplace=False)
    # remove empty columns
    df.dropna(axis=1, how='all', inplace=True)

    # convert to datetime format
    df['StartDate'] = pd.to_datetime(df['StartDate'], format='%d-%m-%Y %H:%M:%S')
    df['EndDate'] = pd.to_datetime(df['EndDate'], format='%d-%m-%Y %H:%M:%S')
    return df
    
def boolean_date_plot(dataframe):
    # df_trim= dataframe.set_index(['Reason'],\
    #     drop=True).loc['Trimproblem'].copy() 
    plt.plot(dataframe.StartDate, np.ones(len(dataframe.StartDate)),'*', label="")
    myFmt = mdates.DateFormatter('%d/%m %H:%M') # select format of datetime
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.show()

# def plotData(dataframe):
#     pass

def check_datetime_for_problem(dataframe,datetime):
    # check if specific point in time had any problem
    # return boolean value and Reason

    return problem_bool, reasondescription

if __name__ == '__main__':
    main()