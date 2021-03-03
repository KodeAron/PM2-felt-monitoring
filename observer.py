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

# global variables
path_data = '../data_observer/'
path_features = '../featuresPerPosition/' # file path folder containing the features files


def main():
    sensorPosition = 'P001F'
    timePeriod = '201027-210221'
    # dataUFF_to_featuresFile(sensorPosition, timePeriod)
    # featuresDF = dataUFF_to_featuresFile(sensorPosition, timePeriod)
    # print(data[0])
    # # plotSignal(data, 4)
    # print(featuresDF.loc[4])
    # plot_features(featuresDF)
    # testlist = convert_data('201027-210221')
    # testlist=load_data(timePeriod=timePeriod)
    # print(testlist)
    # plot_features('test')
    plot_signal('P001F','201205')
    
def load_data(sensorPositions=[],timePeriod=''):
# Load data from files if available. Return list of dataframes, one for each position.
    listOfDataframes = []
    # search through folder for filenames
    dirs = os.scandir(path_features)
    # if no sensorPositions or timePeriods then convert all files in folder
    if len(sensorPositions)==0 and len(timePeriod)==0:
        for entry in dirs:
            print(entry.name) # testing
            #load dataframe from file
            read_pickle_to_dataframe(listOfDataframes,path_features,entry.name)
        # print('Debug: len(sensorPositions)==0 and len(timePeriod)==0')
    else: # else check if specified sensorPositions are available in folder
        converted_files=[] # save files that are converted
        not_found_sensors = sensorPositions # list with sensors not found in folder
        for entry in dirs:
            sensor_position, time_period = split_filename(entry.name)
            if (sensor_position in not_found_sensors and (len(timePeriod)==0 or timePeriod==time_period)):
                not_found_sensors.remove(sensor_position)
                read_pickle_to_dataframe(listOfDataframes,entry.name)
                converted_files.append(entry.name)
            elif (len(sensorPositions)==0 and timePeriod==time_period):
                read_pickle_to_dataframe(listOfDataframes,entry.name)
                converted_files.append(entry.name)
        print('Not in folder: ',end='') 
        print(sensorPositions)
        print('Loaded files: ',end='')
        print(converted_files)

    return listOfDataframes
    
def read_pickle_to_dataframe(listOfDataframes,filename):
    df = pd.read_pickle(path_features + filename)
    listOfDataframes.append([df,filename])

def convert_data(timePeriod=''):
# load UFF, convert to dataframe (with only interesting fields) and save to files
    # search through folder for filenames
    with os.scandir(path_data) as dirs:
        for entry in dirs:
            sensor_position, time_period = split_filename(entry.name)
            # exclued everything that is not UFF file
            if entry.name.endswith('.UFF') and entry.is_file() :
                # only convert files in specified time period or if none is specified
                if (len(timePeriod)==0 or timePeriod==time_period):
                    dataUFF_to_featuresFile(entry.name)
                    print('Converted:',end=' ')
                    print(entry.name) # print filename for loaded file
                else: #(len(timePeriod)!=0 and timePeriod!=time_period):
                    print('Outside specified time period:',end=' ')
                    print(entry.name)
    
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
        result_filename = path_features + sensorPosition + '_' + timePeriod
        # try:
        featuresDF.to_pickle(result_filename)
        # except:
        #     print('nope')
    return featuresDF

def dataUFF_to_featuresDF(sensorPosition, timePeriod):
    data = read_UFF(path_data + sensorPosition + '_A_' + timePeriod + '.uff')
    featuresDF = features_dataframe(data)
    return featuresDF

def read_UFF(filename):
    uff_file = pyuff.UFF(filename) # Tidssignaler_t.o.m._210221/
    # uff_set1 = uff_file.read_sets(0)
    # print(uff_set1) # print the dictionary for measurement 1
    data = uff_file.read_sets()
    return data

def plot_signal(location, date):
# plot signal by specifying which sensor/file and what date
    # assume location is filename
    for entry in os.scandir(path_data):
        if entry.name.startswith(location):
            print('Extracting signal data from',end=' ')
            print(entry.name,end=' ')
            print('...')
            # data=read_UFF(entry.name)
    # 

def plot_signal_from_data(data, index):
    plt.semilogy(data[index]['x'], np.abs(data[index]['data']))
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [g]')
    # plt.xlim([0,10])
    plt.show()

def plot_features(features):
    if type(features) is list and len(features):
        # unpack if features is list (containing filename/sensorPosition)
        features = features[0]
    if type(features) is pd.DataFrame:
        time = features.Datetime
        RMS = features.RMS
        KURT = features.KURT
    else:
        print('Unknown format for features')
        return
    # plt.plot(features.Datetime.to_pydatetime(),features.RMS,'b-', label="RMS")
    plt.plot(time, RMS,'b-', label="rms")
    plt.plot(time, KURT,'r-', label="kurtosis")
    myFmt = mdates.DateFormatter('%d/%m') # select format of datetime
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.show()

def features_dataframe(data):
    # rms, kurtosis
    featuresDF = pd.DataFrame(columns=['Datetime', 'RMS', 'KURT'])#,'x','data'])

    for i in range(len(data)):
        val_rms = np.sqrt(np.mean(data[i]['data']**2))
        val_kurtosis = spstats.kurtosis(np.abs(data[i]['data']))
        # save the calculated features in dataframe. Get datetime at id3 in data
        featuresDF = featuresDF.append({'Datetime':data[i]['id3'], 
            'RMS':val_rms, 'KURT':val_kurtosis},#, 'x':data[i]['x'], 'data':data[i]['data']},
            ignore_index=True)

    featuresDF['Datetime'] = pd.to_datetime(featuresDF['Datetime'], format='%d-%m-%Y %H:%M:%S')
    return featuresDF


if __name__ == '__main__':
    main()