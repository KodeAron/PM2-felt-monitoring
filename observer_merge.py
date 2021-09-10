# -*- coding: utf-8 -*- python3
""" Merge data from uff and xml observer files to one dataframe

Created on Mar 23 2021 15:48
@author: Aron, Luleå University of Technology
"""
import observer_xml as obsx
import observer_uff as obsu
import numpy as np
import datetime as dt
import pandas as pd

# retrieve file location from observer_xml.py
picklefilepath = '../data_observer/pickles/' + obsx.default_filename

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
    uffdfs = obsu.convert_UFFs()
    
    df = obsx.measurements_info()

    # add data column to df
    df['RawData'] = np.nan
    # add node name column to df
    df['NodeName'] = np.nan
    # save which nodes that have been load to prevent loading duplicates
    loaded_nodes = [] 

    for pos in uffdfs:
        # get position, i.e. which node
        position = pos['position']
        # add space between roller name and F/D
        position_str = position[0:4] + ' ' + position[4]
        # lookup the ID from the name
        IDNode = next(node['IDNode'] for node in nodelist\
            if node["NodeName"].startswith(position_str))

        if IDNode in loaded_nodes:
            continue
        print(position,'=',IDNode)
        # save that the node have been loaded
        loaded_nodes.append(IDNode)

        df_unit = df.loc[df['IDNode']==IDNode,:].copy()
        rawdf = pos['df']

        # raise warning if data already stored in data column
        if df_unit['RawData'].isnull().values.all():
            print("All in df_unit['RawData'] is nan. Ready to write.")
            print('len(df_unit) =',str(len(df_unit)),':',\
                'len(rawdf) =',str(len(rawdf)))
        else:
            print(df_unit[df_unit['RawData'].notnull()])
            raise ValueError('Data appeared in unprocessed meas info.')

        df_unit.drop(labels='RawData',axis=1,inplace=True)

        joined_df = df_unit.join(rawdf.set_index('MeasDate'),on='MeasDate')
        rawdf['MeasDate'] = rawdf['MeasDate'].apply(clock12_to_afternoon)
        # print('rawdf "converted" to 24h =',rawdf)
        joined_24 = df_unit.join(rawdf.set_index('MeasDate'),on='MeasDate')

        # check for overlaps
        indices1 = joined_df.loc[joined_df['RawData'].notnull()].index 
        indices2 = joined_24.loc[joined_24['RawData'].notnull()].index 
        overlap = []
        for elem in indices1:
            if elem in indices2:
                overlap.append(elem)
        if len(overlap)>0:
            print('Warning! Overlap detected. Data may be lost.')
            print(overlap)
            print(joined_df.loc[overlap])
            print(joined_24.loc[overlap])

        joined_df.update(joined_24)
        # add NodeName (as string), in addition to IDNode
        joined_df['NodeName'] = position
        df.update(joined_df)

    df.to_pickle(picklefilepath)
    print(df.head())

def clock12_to_afternoon(datetime):
    hour = datetime.hour
    if hour < 12:
        datetime = datetime.replace(hour=hour+12)
        return datetime
    elif hour == 12:
        datetime = datetime.replace(hour=0)
        return datetime
    else:
        print('Not in 12h clock format?')
        raise ValueError

if __name__ == '__main__':
    main()