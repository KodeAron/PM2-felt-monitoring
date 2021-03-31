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
protakdf = pd.DataFrame

def main():
    # filename = '../data_protak/ProTAK PM2 Pressektion 201001-210228.xlsx'
    df = load_data()
    # print(df[df.Reason=='Trimproblem'])
    # boolean_date_plot(df)
    dtdf = pd.DataFrame({'year': [2020, 2021],'month': [11, 3],'day': [4, 5],'hours':[13, 15]})
    dtdf = pd.to_datetime(dtdf)
    date = dtdf.iloc[0]
    boolval = check_datetime_for_problem(date,problem='Trimproblem')
    print('Problem at',date,'?',boolval)

def load_data(filename=protakfilepath):
    # , reasonfilter=['Trimproblem']):
    
    # read operation data from spreadsheet and return as dataframe
    df = pd.read_excel(filename,header=6)
    # create new df fitlered on Reason in reasonfilter
    # Trimproblem, Massakladd, Hål. More relevant Reason ??
    # df = df[df.Reason.isin(reasonfilter)].reset_index(drop=True,inplace=False)
    # remove empty columns
    df.dropna(axis=1, how='all', inplace=True)

    # convert to datetime format
    df['StartDate'] = pd.to_datetime(df['StartDate'], format='%d-%m-%Y %H:%M:%S')
    df['EndDate'] = pd.to_datetime(df['EndDate'], format='%d-%m-%Y %H:%M:%S')
    global protakdf
    protakdf = df
    return df
    
def boolean_date_plot(dataframe):
    # df_trim= dataframe.set_index(['Reason'],\
    #     drop=True).loc['Trimproblem'].copy() 
    plt.plot(dataframe.StartDate, np.ones(len(dataframe.StartDate)),'*', label="")
    myFmt = mdates.DateFormatter('%d/%m %H:%M') # select format of datetime
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.show()

def check_datetime_for_problem(datetime,problem='Trimproblem'):
    # check if specific point in time had specified problem
    # return boolean value and Reason
    df = check_datetime_for_log_entries(datetime)
    print(df)
    # reduce df to the rows for the specific problem
    df = df[df.Reason == problem].reset_index(drop=True,inplace=False)

    if df.empty:
        problem_bool=False
    else:
        problem_bool=True

    return problem_bool

def check_datetime_for_log_entries(datetime):
    # check if datetime has any log entries in the protak file
    # return dataframe
    global protakdf
    if protakdf.empty:
        print('<check_datetime_for_log_entries>',end='')
        print('Empty df. Check if you have run load_data().')
    else:
        # # reduce protakdf to selected columns
        # df = protakdf[['StartDate','EndDate','Reason']
        # create df with all (at most one?) rows containing the specified problem
        df = protakdf.loc[(protakdf.StartDate<datetime) & (datetime<protakdf.EndDate)]
        return df
    

if __name__ == '__main__':
    main()