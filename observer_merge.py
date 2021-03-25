# -*- coding: utf-8 -*- python3
""" Merge data from uff and xml observer files

Created on Mar 23 2021 15:48
@author: Aron, Luleå University of Technology
"""
import observer_xml as obsx
import observer_uff as obsu
import numpy as np
import datetime as dt
import pandas as pd

def main():
    # save_raw_data()
    testing_df_join()

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

    for pos in uffdfs:
        # get position, i.e. which node
        position = pos['position']
        # add space between roller name and F/D
        position_str = position[0:4] + ' ' + position[4]
        # lookup the ID from the name
        IDNode = next(node['IDNode'] for node in nodelist if node["NodeName"].startswith(position_str))
        print(position,'>',IDNode)

        df_unit = df.loc[df['IDNode']==IDNode,:].copy()
        rawdf = pos['featuresDF']

        # raise warning if data already stored in data column
        if df_unit['RawData'].isnull().values.all():
            print("All in df_unit['RawData'] is nan. Ready to write.")
            print('len(df_unit) =',str(len(df_unit)),':','len(rawdf) =',str(len(rawdf)))
        else:
            print(df_unit[df_unit['RawData']!=np.nan])
            raise ValueError('Data appeared in unprocessed measurement info.')

        df_unit.drop(labels='RawData',axis=1,inplace=True)

        # join data where time matches exactly
        joined_df = df_unit.join(rawdf.set_index('MeasDate'),on='MeasDate')
        rawdf['MeasDate'] = rawdf['MeasDate'] + dt.timedelta(hours=12)
        # join data where time differs by +12 h
        joined_pos = df_unit.join(rawdf.set_index('MeasDate'),on='MeasDate')
        rawdf['MeasDate'] = rawdf['MeasDate'] + dt.timedelta(days=-1)# hours=12 already added, net is -12 h
        # join data where time differs by -12 h
        joined_neg = df_unit.join(rawdf.set_index('MeasDate'),on='MeasDate')
        # print(joined_neg)

        joined_df.update(joined_pos,errors='raise')
        joined_df.update(joined_neg,errors='raise')
        df.update(joined_df,errors='raise')
        print('joined_df =',str(joined_df))

    print(df)

def testing_df_join():
    df = pd.DataFrame({'date': [\
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
    unit26 = pd.DataFrame({'date': [dt.datetime(2021,3,20,9,2),dt.datetime(2021,3,21,9,16),\
        dt.datetime(2021,3,22,11,54),dt.datetime(2021,3,23,2,31),dt.datetime(2021,3,24,11,41),\
            dt.datetime(2021,3,25,8,1),dt.datetime(2021,3,26,3,0),dt.datetime(2021,3,27,7,33)],\
                'data':[i+0.26 for i in range(8)]})
    # unit 15, in 12-hour clock
    unit15 = pd.DataFrame({'date': [dt.datetime(2021,3,20,9,17),dt.datetime(2021,3,21,9,16),\
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
        # joined_df = df_unit.join(other.set_index('date'),on='date')
        # print('joined_df',joined_df)
        # other['date'] = other['date'] + dt.timedelta(hours=12)
        # print('+12 h other =',other)
        # joined_pos = df_unit.join(other.set_index('date'),on='date')
        # print('joined_pos',joined_pos)
        # other['date'] = other['date'] + dt.timedelta(days=-1)# hours=12 already added, net is -12 h
        # print('-12 h other =',other)
        # joined_neg = df_unit.join(other.set_index('date'),on='date')
        # print('joined_neg',joined_neg)

        # joined_df = df.join(other.set_index(['date','unit']),on=['date','unit'])
        # other['date'] = other['date'] + dt.timedelta(hours=12)
        # print(other.head())
        # joined_12 = df.join(other.set_index(['date','unit']),on=['date','unit'])
        # print(joined_df)
        # print(joined_12)

        # print('original other =',other)
        joined_df = df_unit.join(other.set_index('date'),on='date')
        # print('joined_df',joined_df)
        other['date'] = other['date'].apply(clock12_to_afternoon)
        # print('other "converted" to 24h =',other)
        joined_24 = df_unit.join(other.set_index('date'),on='date')
        # print('joined_pos',joined_24)

        joined_df.update(joined_24)
        df.update(joined_df)
        print('joined_df =',str(joined_df))
    print(df)

def testing_update():
    pass

def clock12_to_afternoon(datetime):
    # print(type(datetime),end='')
    hour = datetime.hour
    if hour < 12:
        datetime = datetime.replace(hour=hour+12)
        print(datetime)
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