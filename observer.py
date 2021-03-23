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
import datetime as dt

import generaltools as gtol

# global variables
path_uffs = '../data_observer/uff/'
path_pickles = '../data_observer/pickles/' # file path folder containing the features files
# point_click = tuple() # holds the location of the latest click on line in plot


def main():
    position = 'P001F'
    timeperiod = '201027-210221'
    # convert_UFFs('201027-210221')
    # print(testlist)
    # df = UFFfile_to_featuresDF(position,timeperiod)
    df = load_data([position],timeperiod)
    print(df[0]['featuresDF'].RAW[121][5])
    # date = dt.datetime(2020,12,5,12)
    # datetime_list = [dt.datetime(2020,11,5,6,0), dt.datetime(2020,12,3,15,15),dt.datetime(2020,12,7,0,15)]
    # plot_features(df[0])
    # if len(gtol.point_click) > 0:
    #     clicked_time = gtol.point_click[0]
    #     print('clicked time point ',end='')
    #     print(clicked_time)
    #     print(df[0]['featuresDF'].Datetime[0] == clicked_time)
    # print(df[0]['featuresDF']['Datetime'].iloc[0])
    # print(df[0]['featuresDF']['KURT'])
    # print(gtol.count_breaches(df[0]['featuresDF']['KURT'],-0.5,2))

    # # AM/PM issue
    # data=UFFfile_to_UFFdata(position + '_A_' + timeperiod + '.uff')
    # rsp_list = gtol.all_values_from_key(data,'rsp_node')
    # print(rsp_list)

    # # print(measurements_when(data))
    # dict1 = extract_UFFdict_from_date(data,'10-02-2021') # 13:00:07
    # dict2 = extract_UFFdict_from_date(data,'11-02-2021') # 12:00:32
    # gtol.compare_dicts(dict1,dict2)
    # dict1 = extract_UFFdict_from_date(data,'06-02-2021') # 13:23:15
    # dict2 = extract_UFFdict_from_date(data,'30-01-2021') # 01:00:32
    # gtol.compare_dicts(dict1,dict2)
    
def load_data(positions=[],timeperiod=''):
# Load data from files if available. Return list of dataframes, one for each position.
    listOfDataframes = []
    # search through folder for filenames
    dirs = os.scandir(path_pickles)
    # if no positions or timeperiod then convert all files in folder
    if len(positions)==0 and len(timeperiod)==0:
        for entry in dirs:
            print(entry.name) # testing
            #load dataframe from file
            read_pickle_to_dataframe(listOfDataframes,path_pickles,entry.name)
    else: # else check if specified positions are available in folder
        converted_files=[] # save files that are converted
        not_found_sensors = positions # list with sensors not found in folder
        for entry in dirs:
            sensor_position, time_period = split_filename(entry.name)
            if (sensor_position in not_found_sensors and (len(timeperiod)==0 or timeperiod ==time_period)):
                not_found_sensors.remove(sensor_position)
                read_pickle_to_dataframe(listOfDataframes,entry.name)
                converted_files.append(entry.name)
            elif (len(positions)==0 and timeperiod==time_period):
                read_pickle_to_dataframe(listOfDataframes,entry.name)
                converted_files.append(entry.name)
        print('Not in folder: ',end='') 
        print(positions)
        print('Loaded files: ',end='')
        print(converted_files)

    return listOfDataframes
    
def read_pickle_to_dataframe(listOfDataframes,filename):
    df = pd.read_pickle(path_pickles + filename)
    position,timeperiod = split_filename(filename)
    listOfDataframes.append({'featuresDF':df, 'position':position, 'timeperiod':timeperiod})

def convert_UFFs(timeperiod=''):
# load UFF, convert to dataframe (with only interesting fields) and save to files
    # search through folder for filenames
    with os.scandir(path_uffs) as dirs:
        for entry in dirs:
            sensor_position, time_period = split_filename(entry.name)
            # exclued everything that is not UFF file
            if entry.name.endswith('.UFF') and entry.is_file() :
                # only convert files in specified time period or if none is specified
                if (len(timeperiod)==0 or timeperiod==time_period):
                    UFFfile_to_featuresfile(entry.name)
                    print('Converted:',end=' ')
                    print(entry.name) # print filename for loaded file
                else: #(len(timeperiod)!=0 and timeperiod!=time_period):
                    print('Outside specified time period:',end=' ')
                    print(entry.name)
    
def split_filename(filename):
    splitted = filename.split('.')[0].split('_')
    sensor_position = splitted[0]
    # data_type = splitted[1] # ex. A for acceleration
    time_period = splitted[-1] # last element
    return sensor_position, time_period

def UFFfile_to_featuresfile(sensPos_or_filename, timeperiod=''):
# read an UFF file, create features dataframe and save 
    in1len = len(sensPos_or_filename)
    if in1len<5 or (in1len==5 and len(timeperiod)!=13):
        # return error code if to short or missing timeperiod when position is given
        featuresDF=-1     
    else:
        if in1len>5:
        # if position is long then treat as filename
            position,timeperiod = split_filename(sensPos_or_filename)
        else:
            sensPos_or_filename = position
        featuresDF = UFFfile_to_featuresDF(position, timeperiod)
        result_filename = path_pickles + position + '_' + timeperiod
        featuresDF.to_pickle(result_filename)
    return featuresDF

def UFFfile_to_featuresDF(position, timeperiod):
    data = UFFfile_to_UFFdata(path_uffs + position + '_A_' + timeperiod + '.uff')
    featuresDF = UFFdata_to_featuresDF(data)
    return featuresDF

def UFFfile_to_UFFdata(filename):
    if not filename.startswith('../'):
        filename = path_uffs + filename
    uff_file = pyuff.UFF(filename)
    UFFdata = uff_file.read_sets()
    return UFFdata

def UFFdata_to_featuresDF(UFFdata):
    # rms, kurtosis
    featuresDF = pd.DataFrame(columns=['Datetime', 'RAW', 'RMS', 'KURT'])#,'x','data'])

    for i in range(len(UFFdata)):
        val_raw = UFFdata[i]['data']
        val_rms = np.sqrt(np.mean(UFFdata[i]['data']**2))
        val_kurtosis = spstats.kurtosis(np.abs(UFFdata[i]['data']))
        # save the calculated features in dataframe. Get datetime at id3 in data
        featuresDF = featuresDF.append({'Datetime':UFFdata[i]['id3'], 'RAW':val_raw,
            'RMS':val_rms, 'KURT':val_kurtosis},#, 'x':data[i]['x'], 'data':data[i]['data']},
            ignore_index=True)

    featuresDF['Datetime'] = pd.to_datetime(featuresDF['Datetime'], format='%d-%m-%Y %H:%M:%S')
    return featuresDF

def plot_signal(location, datestring):
# plot signal by specifying which sensor/file and what date
# datestring as 'DD-MM-YYYY'
    # assume location is filename
    file_found=False
    for entry in os.scandir(path_uffs):
        if entry.name.startswith(location):
            file_found=True
            print('Extracting signal data from',end=' ')
            print(entry.name,end=' ')
            print('...')
            dicts = read_UFF(entry.name)
            # check which datetime string ('id3' in the data dict) that 
            # starts with the requested date
            index = next((i for i, item in enumerate(dicts) if item['id3'].startswith(datestring)), None)
            print(index)
            plot_signal_from_data(dicts,index)
            break # escape loop when one file is found
    if not file_found:
        print('Could not retrieve data. Check spelling and that the file is available in',end=' ')
        print(path_uffs)

def plot_signal_from_data(data, index):
    fig, ax = plt.subplots()
    tolerance = 5 # points
    ax.plot(data[index]['x'], data[index]['data'],'b-', label='acceleration',picker=tolerance)
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [g]')
    # plt.xlim([0,10])
    plt.title(data[index]['id3'])
    # print(data[index])
    fig.canvas.callbacks.connect('pick_event', on_pick)
    plt.show()

def plot_features(features):
    fig, ax = plt.subplots()
    tolerance = 5 # points
    if type(features) is dict and len(features):
    # unpack if features is dict (containing featuresDF, position and timeperiod)
        features = features['featuresDF']
    if type(features) is pd.DataFrame:
        Datetime = features.Datetime
        RMS = features.RMS
        KURT = features.KURT
    else:
        print('Unknown format for features')
        return
    # ax.plot(Datetime.dt.to_pydatetime(),RMS,'b-', label="RMS")
    ax.plot(Datetime, RMS,'b-', label="rms",picker=True)
    ax.plot(Datetime, KURT,'r-', label="kurtosis",picker=True)
    myFmt = mdates.DateFormatter('%d/%m') # select format of datetime
    plt.gca().xaxis.set_major_formatter(myFmt)
    fig.canvas.callbacks.connect('pick_event', gtol.on_pick)
    plt.show()

def measurements_when(UFFdata):
    # extract all date/times for when the measurements were done
    datetime_list = []
    for item in UFFdata:
        datetime_list.append(item['id3'])
    return datetime_list

def extract_UFFdict_from_date(UFFdata, datestring):
    index = next((i for i, item in enumerate(UFFdata) if item['id3'].startswith(datestring)), None)
    return UFFdata[index]

if __name__ == '__main__':
    main()