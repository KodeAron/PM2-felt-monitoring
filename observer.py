# -*- coding: utf-8 -*- python3
""" Accelerometer data reader

Read acceleration data in UFF format. Return dataframe. Save to file.

Created on Feb 25 2021 11:30
@author: Aron, Luleå University of Technology
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pyuff
import csv # no installation needed?
import scipy.stats as spstats
import pandas as pd
import os

def main():
    sensorPosition = 'P001F'
    timePeriod = '201027-210221'
    # dataUFF_to_featuresFile(sensorPosition, timePeriod)
    # featuresDF = dataUFF_to_featuresFile(sensorPosition, timePeriod)
    # print(data[0])
    # # plotSignal(data, 4)
    # print(featuresDF.loc[4])
    # plot_features(featuresDF)
    testlist = convert_data()
    print(testlist)
    load_data()
    
def load_data(sensorPositions=[]):
# Load data from files if available. Return list of dataframes, one for each position.
    #load dataframe from file
    df = pd.read_pickle(r"..\featuresPerPosition\P001F_201027-210221")

    #print dataframe
    print(df.data[1])
    print(df.data[1][35])
    # return listOfDataframes

def convert_data(sensorPositions=[],timePeriod=''):
# load UFF, convert to dataframe (with only interesting fields) and save to files
# sensorPositions: list of sensor positions that should be retrieved
    path_source = r"..\data_observer"
    # path_result = r"..\featuresPerPosition"
    listOfDataframes = []
    if len(sensorPositions)==0 and len(timePeriod)==0: 
    # if no sensorPositions or timePeriods
    # then convert all files in folder
        # search through folder for filenames
        with os.scandir(path_source) as dirs:
            for entry in dirs:
                # exclued everything that is not UFF file
                if entry.name.endswith('.UFF') and entry.is_file():
                    print(entry.name) # testing
                    # sensor_position, time_period = split_filename(entry.name)
                    listOfDataframes.append(dataUFF_to_featuresFile(entry.name))

    # dataUFF_to_featuresFile(sensorPositions[0],'201027-210221')
    return listOfDataframes
    
def split_filename(filename):
    splitted = filename.split('.')[0].split('_')
    sensor_position = splitted[0]
    # data_type = splitted[1] # ex. A for acceleration
    time_period = splitted[-1] # last element
    return sensor_position, time_period

def dataUFF_to_featuresFile(sensPos_or_filename, timePeriod=''):
# read an UFF file, create features dataframe and save 
    in1len = len(sensPos_or_filename)
    if in1len<5 or (in1len==5 and len(timePeriod)!=13):
        # return error code if to short or missing timePeriod when sensorPosition is given
        featuresDF=-1     
    else:
        if in1len>5:
        # if sensorPosition is long then treat as filename
            sensorPosition,timePeriod = split_filename(sensPos_or_filename)
        else:
            sensPos_or_filename = sensorPosition
        featuresDF = dataUFF_to_featuresDF(sensorPosition, timePeriod)
        result_filename = '../featuresPerPosition/' + sensorPosition + '_' + timePeriod
        # try:
        featuresDF.to_pickle(result_filename)
        # except:
        #     print('nope')
    return featuresDF

def dataUFF_to_featuresDF(sensorPosition, timePeriod):
    data = read_UFF('../data_observer/' + sensorPosition + '_A_' + timePeriod + '.uff')
    featuresDF = features_dataframe(data)
    return featuresDF

def read_UFF(filename):
    uff_file = pyuff.UFF(filename) # Tidssignaler_t.o.m._210221/
    # uff_set1 = uff_file.read_sets(0)
    # print(uff_set1) # print the dictionary for measurement 1
    data = uff_file.read_sets()
    return data

def plot_signal(data, index):
    plt.semilogy(data[index]['x'], np.abs(data[index]['data']))
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [g]')
    # plt.xlim([0,10])
    plt.show()

def plot_features(features):
    if type(features) is np.array:
        plt.plot(features[:,0],'b-', label="rms")
        plt.plot(features[:,1],'r-', label="kurtosis")
        plt.show()
    elif type(features) is pd.DataFrame:
        # plt.plot(features.Datetime.to_pydatetime(),features.RMS,'b-', label="RMS")
        plt.plot(features.Datetime, features.RMS,'b-', label="rms")
        plt.plot(features.Datetime, features.KURT,'r-', label="kurtosis")
        myFmt = mdates.DateFormatter('%d/%m') # select format of datetime
        plt.gca().xaxis.set_major_formatter(myFmt)
        plt.show()
    else:
        print('Unknown format for features')

def features_dataframe(data):
    # rms, kurtosis
    featuresDF = pd.DataFrame(columns=['Datetime', 'RMS', 'KURT','x','data'])

    for i in range(len(data)):
        val_rms = np.sqrt(np.mean(data[i]['data']**2))
        val_kurtosis = spstats.kurtosis(np.abs(data[i]['data']))
        # save the calculated features in dataframe. Get datetime at id3 in data
        featuresDF = featuresDF.append({'Datetime':data[i]['id3'], 
            'RMS':val_rms, 'KURT':val_kurtosis, 'x':data[i]['x'], 'data':data[i]['data']},
            ignore_index=True)

    featuresDF['Datetime'] = pd.to_datetime(featuresDF['Datetime'], format='%d-%m-%Y %H:%M:%S')
    return featuresDF


if __name__ == '__main__':
    main()