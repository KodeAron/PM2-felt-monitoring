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

    for pos in uffdfs:
        # add space between roller name and F/D
        position = pos['position']
        position_str = position[0:4] + ' ' + position[4]
        # lookup the ID from the name
        IDNode = next(node['IDNode'] for node in nodelist if node["NodeName"].startswith(position_str))
        print(IDNode)

        # get all row indices that belongs to the node
        noderows = df.loc[(df['IDNode'] == IDNode)].index 

        # print(type(df.iloc[noderows].MeasDate.iloc[0]))
        # print(type(pos['featuresDF'].MeasDate.iloc[0]))

        dates_df = df.iloc[noderows[0:len(pos['featuresDF'])]]['MeasDate'].reset_index(drop=True)
        dates_pos = pos['featuresDF']['MeasDate'].reset_index(drop=True)
        # print(dates_df)
        # print(dates_pos)

        # date_match = (dates_df == dates_pos + dates_df-dates_pos == dt.timedelta(hours=12) + \
        #     dates_pos-dates_df == dt.timedelta(hours=12))

        diff_array = dates_df-dates_pos
        # print(diff_array)

        acceptable_diff = np.array([dt.timedelta(hours=0),dt.timedelta(hours=12),\
            dt.timedelta(days=-1,hours=12)], dtype="timedelta64[ms]")

        match_dates = np.isin(diff_array,acceptable_diff)

        if match_dates.all():
            print("All 'MeasDate' match.")
        else:
            print("One or more 'MeasDate' does not match.")
            for ind in range(len(match_dates)):
                if not match_dates[ind]:
                    print(dates_df[ind], end=' vs ')
                    print(dates_pos[ind])

        # print(date_match)

        # match_0 = df.iloc[noderows[0:len(pos['featuresDF'])]][['MeasDate']].reset_index(drop=True)\
        #      == pos['featuresDF'][['MeasDate']].reset_index(drop=True)
             
        # pos_p12 = pos['featuresDF'][['MeasDate']] + pd.DateOffset(hours=12)
        # match_p12 = df.iloc[noderows[0:len(pos['featuresDF'])]][['MeasDate']].reset_index(drop=True)\
        #      == pos_p12.reset_index(drop=True)
        # pos_m12 = pos['featuresDF'][['MeasDate']] - pd.DateOffset(hours=12)
        # match_m12 = df.iloc[noderows[0:len(pos['featuresDF'])]][['MeasDate']].reset_index(drop=True)\
        #      == pos_m12.reset_index(drop=True)
        # match_df = df.loc[np.all(df.iloc[noderows[0:len(pos['featuresDF'])-1]][['MeasDate']].values == pos['featuresDF'][['MeasDate']].values, axis=0)]
        # match=pd.DataFrame(columns=['MeasDate'])
        # match = np.any(match_0['MeasDate'].to_numpy(),match_p12['MeasDate'].to_numpy(),match_m12['MeasDate'].to_numpy())
        # print(match)

        # df = df.loc[np.all(df.values == df.values, axis=1),:]

        # print(df.iloc[noderows][['MeasDate']].values == pos['featuresDF'][['MeasDate']].values)
        # df['RawData'] = np.where((df.iloc[noderows][['MeasDate']].values == pos['featuresDF'][['MeasDate']].values),
        # 'equal', 'nope')

        # print(len(matching_time),'/',len(pos['featuresDF']))

        # df.at[noderows,'RawData'] = noderows

        # print(noderows)
        # print(df.iloc[7:10])

        # diff = df.iloc[noderows[0]].MeasDate-pos['featuresDF'].iloc[-1].MeasDate

        # if diff < dt.timedelta(milliseconds=10):
        #     print('less than 10 ms diff')

        # df.iloc[0]['RawData'] = 'test'

        # print(df[df['RawData']=='test'])
        
    print(df)

if __name__ == '__main__':
    main()