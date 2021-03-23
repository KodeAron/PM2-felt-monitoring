# -*- coding: utf-8 -*- python3
""" Merge data from uff and xml observer files

Created on Mar 23 2021 15:48
@author: Aron, Luleå University of Technology
"""
import observer_xml as obsx
import observer_uff as obsu
import numpy as np

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
        for node in nodelist:
            if node['NodeName'].startswith(position_str):
                print(node['IDNode'])
                break

if __name__ == '__main__':
    main()