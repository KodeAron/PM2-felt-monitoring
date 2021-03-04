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

# global variables
path_data = '../data_observer/'
path_features = '../featuresPerPosition/' # file path folder containing the features files


def main():
    # sensorPosition = 'P001F'
    # timePeriod = '201027-210221'
    # testlist = convert_UFFs('201027-210221')
    UFFdata = 
    df = UFFdata_to_featuresDF(UFFdata)
    date = dt.datetime(2020,12,5,12)
    # datetime_list = [dt.datetime(2020,11,5,6,0), dt.datetime(2020,12,3,15,15),dt.datetime(2020,12,7,0,15)]
    # plot_signal('testar','')
    nearest_date, date_diff = nearest(df.Datetime,date)
    print(nearest_date)
    print(date_diff)
    
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

def convert_UFFs(timePeriod=''):
# load UFF, convert to dataframe (with only interesting fields) and save to files
    # search through folder for filenames
    with os.scandir(path_data) as dirs:
        for entry in dirs:
            sensor_position, time_period = split_filename(entry.name)
            # exclued everything that is not UFF file
            if entry.name.endswith('.UFF') and entry.is_file() :
                # only convert files in specified time period or if none is specified
                if (len(timePeriod)==0 or timePeriod==time_period):
                    UFFfile_to_featuresfile(entry.name)
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

def UFFfile_to_featuresfile(sensPos_or_filename, timePeriod=''):
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
        featuresDF = UFFfile_to_featuresDF(sensorPosition, timePeriod)
        result_filename = path_features + sensorPosition + '_' + timePeriod
        featuresDF.to_pickle(result_filename)
    return featuresDF

def UFFfile_to_featuresDF(sensorPosition, timePeriod):
    data = UFFfile_to_UFFdata(path_data + sensorPosition + '_A_' + timePeriod + '.uff')
    featuresDF = UFFdata_to_featuresDF(data)
    return featuresDF

def UFFfile_to_UFFdata(filename):
    if not filename.startswith('../'):
        filename = path_data + filename
    uff_file = pyuff.UFF(filename)
    UFFdata = uff_file.read_sets()
    return UFFdata

def UFFdata_to_featuresDF(UFF_data):
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

def plot_signal(location, datestring):
# plot signal by specifying which sensor/file and what date
# datestring as 'DD-MM-YYYY'
    # assume location is filename
    file_found=False
    for entry in os.scandir(path_data):
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
        print(path_data)

def plot_signal_from_data(data, index):
    fig, ax = plt.subplots()
    tolerance = 5 # points
    ax.plot(data[index]['x'], data[index]['data'],'b-', label='acceleration',picker=tolerance)
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [g]')
    # plt.xlim([0,10])
    plt.title(data[index]['id3'])
    print(data[index])
    fig.canvas.callbacks.connect('pick_event', on_pick)
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
    
def on_pick(event):
    artist = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    x, y = artist.get_xdata(), artist.get_ydata()
    ind = event.ind
    print('Artist picked:', event.artist)
    print('{} vertices picked'.format(len(ind)))
    print('Pick between vertices {} and {}'.format(min(ind), max(ind)+1))
    print('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
    print('Data point:', x[ind[0]], y[ind[0]])
    print()

def closest_to_date(collection_of_dates, datetime):
    if type(collection_of_dates)==list:
        pass
    else:
        print('Unknown type')

def nearest(items, pivot):
    nearest = min(items, key=lambda x: abs(x - pivot))
    timedelta = abs(nearest - pivot)
    return nearest, timedelta

if __name__ == '__main__':
    main()