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

picklefilepath = '../data_observer/pickles/' + obsx.default_filename #'1aPressT_Acc_ej-nyp_201015-210325'

def main():
    save_raw_data()
    # testing_df_join()

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

    # add data column to df
    df['RawData'] = np.nan
    loaded_nodes = [] # save which nodes that have been load to prevent loading duplicates.

    for pos in uffdfs:
        # get position, i.e. which node
        position = pos['position']
        # add space between roller name and F/D
        position_str = position[0:4] + ' ' + position[4]
        # lookup the ID from the name
        IDNode = next(node['IDNode'] for node in nodelist if node["NodeName"].startswith(position_str))
        if IDNode in loaded_nodes:
            continue # skip to next position. 
            # Beware that this may meen skipping data that has not been loaded if the 
            # raise ValueError('Loaded node that have already been merged.')
        print(position,'=',IDNode)
        loaded_nodes.append(IDNode) # save that the node have been loaded

        df_unit = df.loc[df['IDNode']==IDNode,:].copy()
        rawdf = pos['df']

        # raise warning if data already stored in data column
        if df_unit['RawData'].isnull().values.all():
            print("All in df_unit['RawData'] is nan. Ready to write.")
            print('len(df_unit) =',str(len(df_unit)),':','len(rawdf) =',str(len(rawdf)))
        else:
            print(df_unit[df_unit['RawData'].notnull()])
            raise ValueError('Data appeared in unprocessed measurement info.')

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
        df.update(joined_df)

    df.to_pickle(picklefilepath)
    print(df.head())

def testing_df_join():
    df = pd.DataFrame({'MeasDate': [\
                dt.datetime(2021,3,20,21,2),dt.datetime(2021,3,21,9,16),\
        dt.datetime(2021,3,22,23,54),dt.datetime(2021,3,23,14,31),dt.datetime(2021,3,24,11,41),\
            dt.datetime(2021,3,25,20,1),dt.datetime(2021,3,26,15,0),dt.datetime(2021,3,27,7,33),\
                dt.datetime(2021,3,20,21,17),dt.datetime(2021,3,21,9,16),\
        dt.datetime(2021,3,22,23,17),dt.datetime(2021,3,23,14,11),dt.datetime(2021,3,24,11,13),\
            dt.datetime(2021,3,25,20,52),dt.datetime(2021,3,26,12,2),dt.datetime(2021,3,27,0,2)],\
                'unit':['26' for i in range(8)] + [ '15' for i in range(8)],
                'info':['Some info on measurement' for i in range(16)]})
    # other = pd.DataFrame({'date': [dt.datetime(2021,3,20,21,17),dt.datetime(2021,3,21,9,16),\
    #         dt.datetime(2021,3,25,20,52),dt.datetime(2021,3,26,15,23),dt.datetime(2021,3,27,7,2),\
    #     dt.datetime(2021,3,22,23,17),dt.datetime(2021,3,23,14,11),dt.datetime(2021,3,24,11,13)],\
    #             'data':[np.random.rand() for i in range(8)]})
    # unit 26, in 12-horu clock
    unit26 = pd.DataFrame({'MeasDate': [dt.datetime(2021,3,20,9,2),dt.datetime(2021,3,21,9,16),\
        dt.datetime(2021,3,22,11,54),dt.datetime(2021,3,23,2,31),dt.datetime(2021,3,24,11,41),\
            dt.datetime(2021,3,25,8,1),dt.datetime(2021,3,26,3,0),dt.datetime(2021,3,27,7,33)],\
                'data':[i+0.26 for i in range(8)]})
    # unit 15, in 12-hour clock
    unit15 = pd.DataFrame({'MeasDate': [dt.datetime(2021,3,20,9,17),dt.datetime(2021,3,21,9,16),\
        dt.datetime(2021,3,22,11,17),dt.datetime(2021,3,23,2,11),dt.datetime(2021,3,24,11,13),\
            dt.datetime(2021,3,25,8,52),dt.datetime(2021,3,26,12,2),dt.datetime(2021,3,27,12,2)],\
                'data':[i+0.15 for i in range(8)]})

    units = [{'name':'15','df':unit15}, {'name':'26','df':unit26}]

    # add data column to df
    df['data'] = np.nan
    # for testing ValueError exception
    # df['data'] = [i+0.89 for i in range(len(df))]

    # add unit column to other
    # other['unit'] = '12'

    for unit in units:
        unitname = unit['name']
        print('Unit name =',unitname)
        # df_unit will keep index, important! i.e. no reindexing
        df_unit = df.loc[df['unit']==unitname,:].copy()
        other = unit['df']

        # raise warning if data already stored in data column
        if df_unit['data'].isnull().values.all():
            print('all nan')
        else:
            print(df_unit[df_unit['data']!=np.nan])
            raise ValueError('Data appeared in unprocessed measurement info.')

        df_unit.drop(labels='data',axis=1,inplace=True)

        # print('original other =',other)
        joined_df = df_unit.join(other.set_index('MeasDate'),on='MeasDate')
        print('joined_df',joined_df)
        other['MeasDate'] = other['MeasDate'].apply(clock12_to_afternoon)
        # print('other "converted" to 24h =',other)
        joined_24 = df_unit.join(other.set_index('MeasDate'),on='MeasDate')
        print('joined_24',joined_24)

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
        df.update(joined_df)
        print('joined_df =',str(joined_df))
    print(df)

def testing_update():
    pass

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

    # else:
    #     print('clock12_to_afternoon() only accepts datetime obj as input')

if __name__ == '__main__':
    main()