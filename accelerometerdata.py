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

    ### test stuff
    # arr = np.array([[1,2,3,4,5],[6,7,8,9,10]])
    # arr2 = np.array([[11,12,13,14,15]])
    # testArray = np.concatenate((arr,arr2), axis=0)
    # print(testArray)
    # featuresMatrix = np.empty([[2, len(data)]], dtype=float)
    # print(featuresMatrix)
    # print(type(data)) # list
    # print(spstats.kurtosis(np.abs(data[0]['data'])))
    # print('length',len(data))

def dataUFF_to_featuresCSV(sensorPosition, timePeriod):
    featuresDF = dataUFF_to_featuresDF(sensorPosition, timePeriod)
    csvfilename = '../featuresPerPosition/' + sensorPosition + '_' + timePeriod + '.csv'
    featuresDF.to_csv(csvfilename)

def dataUFF_to_featuresDF(sensorPosition, timePeriod):
    data = readUFF('../' + sensorPosition + '_A_' + timePeriod + '.uff')
    featuresDF = featuresAsDataframe(data)
    return featuresDF

def readUFF(filename):
    uff_file = pyuff.UFF('../P001F_A_201027-210221.uff') # Tidssignaler_t.o.m._210221/
    # uff_types = uff_file.get_set_types()
    # print(uff_types)
    # uff_set1 = uff_file.read_sets(0)
    # print(uff_set1)
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
        plt.plot(features.Datetime, features.RMS,'b-', label="RMS")
        plt.plot(features.Datetime, features.Kurtosis,'r-', label="kurtosis")
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

        ## add rows in end of matrix
        # featuresMatrix = np.concatenate((featuresMatrix,new_row), axis=0)
    
    return featuresMatrix

def featuresAsDataframe(data):
    # rms, kurtosis
    featuresDF = pd.DataFrame(columns=['Datetime', 'RMS', 'Kurtosis'])

    for i in range(len(data)):
        pass
        # featuresDict = 
        val_rms = np.sqrt(np.mean(data[i]['data']**2))
        val_kurtosis = spstats.kurtosis(np.abs(data[i]['data']))
        # save the calculated features in dataframe. Get datetime at id3 in data
        featuresDF = featuresDF.append({'Datetime': data[i]['id3'], 'RMS': val_rms, 'Kurtosis': val_kurtosis},\
            ignore_index=True)

    featuresDF['Datetime'] = pd.to_datetime(featuresDF['Datetime'], format='%d-%m-%Y %H:%M:%S')
    return featuresDF


if __name__ == '__main__':
    main()