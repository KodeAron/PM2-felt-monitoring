# -*- coding: utf-8 -*- python3
""" protak data reader

Created on Feb 25 2021 10:10
@author: Aron, Luleå University of Technology
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import math

import generaltools as gtol

protakfilepath = '../data_protak/ProTAK statistics raw PM2 2020-10-30 - 2021-03-26.xlsx'
# protakdf = pd.DataFrame

def main():
    # filename = '../data_protak/ProTAK PM2 Pressektion 201001-210228.xlsx'
    df = load_data()
    # print(df[df.Reason=='Trimproblem'])
    # df = digital_problem_df(df,first_date=pd.datetime(2020,11,4))
    print(df)
    # dtdf = pd.DataFrame({'year': [2020, 2021],'month': [11, 3],'day': [4, 5],'hours':[13, 15]})
    # dtdf = pd.to_datetime(dtdf)
    # date = dtdf.iloc[0]
    # boolval = check_datetime_for_problem(date,problem='Trimproblem')
    # print('Problem at',date,'?',boolval)

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
    # global protakdf
    # protakdf = df
    return df
    
def digital_problem_plot(dataframe,reason='Trimproblem'):
    df = digital_problem_df(dataframe,reason)
    print(df)
    plt.plot(df.Date, df[reason],'-', label="")
    myFmt = mdates.DateFormatter('%d/%m %H:%M') # select format of datetime
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.show()

def digital_problem_df(dataframe='',reason='', first_date=None, last_date=None):
    if len(dataframe)==0:
        dataframe = load_data()
    if reason != '':
        df = dataframe.set_index(['Reason'],\
            drop=True).loc[reason].copy()
    else:
        df = dataframe
    problem_df = pd.DataFrame(columns=['Date', reason])
    end = df.iloc[0].StartDate
    problem_df = problem_df.append({'Date' : end, reason : True}, ignore_index=True)
    for index in range(len(df)):
        start = df.iloc[index].StartDate
        if start != end: # compare start with previous end
            # add False points in between if there is space beween consecutive problem entries
            problem_df = problem_df.append({'Date' : end, reason : False}, ignore_index=True)
            problem_df = problem_df.append({'Date' : start, reason : False}, ignore_index=True)
            problem_df = problem_df.append({'Date' : start, reason : True}, ignore_index=True)
        end = df.iloc[index].EndDate
        problem_df = problem_df.append({'Date' : end, reason : True}, ignore_index=True)
    problem_df = problem_df.append({'Date' : end, reason : False}, ignore_index=True)

    # splice to desired interval
    def is_date_between(checkdate):
        boolval = gtol.is_date_between(checkdate,first_date,last_date)
        return boolval
    problem_df = problem_df[problem_df['Date'].apply(is_date_between)].reset_index(drop=True)
    if last_date is not None:
        problem_df = problem_df.append({'Date' : last_date, reason : False}, ignore_index=True)

    return problem_df

def check_datetime_for_Trimproblem(datetime):
    return check_datetime_for_problem(datetime,problem='Trimproblem')

def check_datetime_for_Massakladd(datetime):
    return check_datetime_for_problem(datetime,problem='Massakladd')

def check_datetime_for_Hal(datetime):
    return check_datetime_for_problem(datetime,problem='Hål')

def check_datetime_for_problem(datetime,problem='Trimproblem'):
    # check if specific point in time had specified problem
    # return boolean value and Reason
    df = check_datetime_for_log_entries(datetime)
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
    
# always run this. import or not.
protakdf = load_data()

if __name__ == '__main__':
    main()
