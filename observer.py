# -*- coding: utf-8 -*- python3
""" Accelerometer data reader

Read acceleration data in UFF format. Return dataframe or matrix. Save to csv.

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

def main():
    sensorPosition = 'P001F'
    timePeriod = '201027-210221'
    # dataUFF_to_featuresCSV(sensorPosition, timePeriod)
    featuresDF = dataUFF_to_featuresDF(sensorPosition, timePeriod)
    # print(data[0])
    # # plotSignal(data, 4)
    # print(featuresDF.loc[4])
    plotFeatures(featuresDF)

def dataUFF_to_featuresCSV(sensorPosition, timePeriod):
    featuresDF = dataUFF_to_featuresDF(sensorPosition, timePeriod)
    csvfilename = '../featuresPerPosition/' + sensorPosition + '_' + timePeriod + '.csv'
    featuresDF.to_csv(csvfilename)

def dataUFF_to_featuresDF(sensorPosition, timePeriod):
    data = readUFF('../data_observer/' + sensorPosition + '_A_' + timePeriod + '.uff')
    featuresDF = featuresAsDataframe(data)
    return featuresDF

def readUFF(filename):
    uff_file = pyuff.UFF(filename) # Tidssignaler_t.o.m._210221/
    # uff_set1 = uff_file.read_sets(0)
    # print(uff_set1) # print the dictionary for measurement 1
    data = uff_file.read_sets()
    return data

def plotSignal(data, index):
    plt.semilogy(data[index]['x'], np.abs(data[index]['data']))
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [g]')
    # plt.xlim([0,10])
    plt.show()

def plotFeatures(features):
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

def featuresAsMatrix(data):
    # rms, kurtosis
    featuresMatrix = np.empty([len(data),2], dtype=float)

    for i in range(len(data)):
        elem_rms = np.sqrt(np.mean(data[i]['data']**2))
        elem_kurtosis = spstats.kurtosis(np.abs(data[i]['data']))
        new_row = np.array([[elem_rms, elem_kurtosis]])
        featuresMatrix[i] = new_row
    
    return featuresMatrix

def featuresAsDataframe(data):
    # rms, kurtosis
    featuresDF = pd.DataFrame(columns=['Datetime', 'RMS', 'KURT'])

    for i in range(len(data)):
        val_rms = np.sqrt(np.mean(data[i]['data']**2))
        val_kurtosis = spstats.kurtosis(np.abs(data[i]['data']))
        # save the calculated features in dataframe. Get datetime at id3 in data
        featuresDF = featuresDF.append({'Datetime': data[i]['id3'], 'RMS': val_rms, 'KURT': val_kurtosis},\
            ignore_index=True)

    featuresDF['Datetime'] = pd.to_datetime(featuresDF['Datetime'], format='%d-%m-%Y %H:%M:%S')
    return featuresDF


if __name__ == '__main__':
    main()