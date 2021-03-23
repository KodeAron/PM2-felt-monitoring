# -*- coding: utf-8 -*- python3
""" Accelerometer data reader

Read acceleration data in xml (xmd/xme) format. Return dataframe. Save to file.

Created on Mar 16 2021 11:30
@author: Aron, Luleå University of Technology
"""
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import scipy.stats as spstats
import pandas as pd
import datetime as dt
import xml.etree.ElementTree as etree
import struct

import generaltools as gtol

# global variables
path_data = '../data_observer/xml/' # folder containing the raw data
path_features = '../data_observer/features_dfs/' # folder containing the features files

def main():
    filename = '1aPressT_Acc_ej-nyp_201001-210315'
    xme_file = filename + '.xme'
    xmd_file = filename + '.xmd'
    # list_of_nodes = nodelist(xme_file)
    # print(list_of_nodes)
    df = measurements_info(xmd_file)
    print(df)
    # plot_signal_from_xmd(xmd_file,'4624','2020-12-18')

def measurements_info(xmdfilename):
    """ 
    Extract all measurements and information; such as MeasID, IDNode, Speed; for each.
    """
    full_path = path_data + xmdfilename
    tree = etree.parse(full_path)
    root = tree.getroot()

    # meas_df = pd.DataFrame()#columns=['User_ID', 'UserName', 'Action'])
    meas_dictlist = []

    for measurement in root.findall('Measurement'):
        measdict = {}
        for child in measurement:
            measdict[child.tag] = child.text
        meas_dictlist.append(measdict)
        # break
    meas_df = pd.DataFrame(meas_dictlist)     
    return meas_df

def plot_signal_from_xmd(xmdfilename, IDNode, datestring):
    full_path = path_data + xmdfilename
    tree = etree.parse(full_path)
    root = tree.getroot()
    
    for measurement in root.findall('Measurement'):
        if measurement.find('IDNode').text == IDNode and measurement.find('MeasDate').text.startswith(datestring):
            print('MeasDate: ' + measurement.find('MeasDate').text)
            IDMeasurement = measurement.find('IDMeasurement').text
            print('IDMeasurement: ' + IDMeasurement)
            break
    
    for MeasurementBinaryRaw in root.findall('MeasurementBinaryRaw'):
        if MeasurementBinaryRaw.find('IDMeasurement').text == IDMeasurement and \
            MeasurementBinaryRaw.find('DataType').text == '2': # DataType=2 means time signal
            scalefactor = float(MeasurementBinaryRaw.find('ScaleFactor').text)
            print('scalefactor = ' + str(scalefactor))
            RawData = MeasurementBinaryRaw.find('RawData').text
            break

    print('len(RawData) = '+str(len(RawData)))
    RawData_bytestring = RawData.encode('iso8859_2')#'utf-8')
    # print(len(RawData))
    # print(len(RawData_bytestring))
    # print(int(RawData_bytestring[0]))

    unpackedData = []

    print('len(RawData_bytestring) = ' + str(len(RawData_bytestring)))

    true_noLines = 16384 # true number of lines, retrieved from 

    for iLine in range(true_noLines):
        offset = (iLine)*2
        value, = struct.unpack_from('=h', RawData_bytestring,offset=offset)
        # value, = struct.unpack_from('=B', RawData_bytestring,offset=iLine)
        # value = int.from_bytes(RawData_bytestring[iLine:(iLine+2)],'little',signed=True)
        unpackedData.append(value)
        
    # print(unpackedData)
    processed_data = scalefactor * np.array(unpackedData)
    print('processed_data = ' + str(processed_data))
    print('len(procesed_data) = ' + str(len(processed_data)))

    print('max value : ' + str(max(unpackedData)))
    print('min value : ' + str(min(unpackedData)))

    plt.plot(processed_data[:],'b*',label='processed data')
    plt.show()


def nodelist(xmefilename):
    full_path = path_data + xmefilename
    tree = etree.parse(full_path)
    root = tree.getroot()

    nodelist = []
    list_of_parents = []

    for node in root.findall('Node'):
        IDNode = node.find('IDNode').text
        IDParent = node.find('IDParent').text
        NodeName = node.find('NodeName').text

        # add to list, as dictionary
        nodedict = {'IDNode':IDNode, 'IDParent':IDParent, 'NodeName':NodeName}
        nodelist.append(nodedict)

        # save IDParents in list
        list_of_parents.append(IDParent)

    # delete all parent nodes, all nodes except those in the "bottom"
    iteration=0
    while iteration < len(nodelist):
        if nodelist[iteration]['IDNode'] in list_of_parents:
            nodelist.pop(iteration)
        else:
            iteration=iteration+1            

    return nodelist

if __name__ == '__main__':
    main()