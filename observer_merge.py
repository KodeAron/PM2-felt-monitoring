# -*- coding: utf-8 -*- python3
""" Merge data from uff and xml observer files

Created on Mar 23 2021 15:48
@author: Aron, Luleå University of Technology
"""
import observer_xml as obsx
import observer_uff as obsu
import numpy as np
import datetime as dt

def main():
    save_raw_data()

def save_raw_data():
    """ Save a dataframe with raw data
    Use pickle to save raw data in dataframe.
    """
    # load a list of dictionaries for positions and their IDs
    nodelist = obsx.nodelist()
     # load a list of dictionaries. 
     # One key holds the dataframe. {featuresDF, position, timeperiod}
    uffdfs = obsu.load_data()
    
    df = obsx.measurements_info()

    df['RawData'] = np.nan
    print(df)

    for pos in uffdfs:
        # add space between roller name and F/D
        position = pos['position']
        position_str = position[0:4] + ' ' + position[4]
        # lookup the ID from the name
        IDNode = next(node['IDNode'] for node in nodelist if node["NodeName"].startswith(position_str))
        print(IDNode)

        noderows = df.loc[(df['IDNode'] == IDNode)].index 

        df.at[noderows,'RawData'] = noderows

        print(noderows)
        print(df.iloc[7:10])

        diff = df.iloc[noderows[0]].MeasDate-pos['featuresDF'].iloc[-1].Datetime

        if diff < dt.timedelta(milliseconds=10):
            print('less than 10 ms diff')
        elif diff < dt.timedelta(seconds=1):
            print('less than 1 s diff')
        elif diff < dt.timedelta(minute=1):
            print('less than 1 min diff')

        print(diff)

        # df.iloc[0]['RawData'] = 'test'

        # df.set_value()

        # print(df[df['RawData']=='test'])

if __name__ == '__main__':
    main()