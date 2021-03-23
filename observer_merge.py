# -*- coding: utf-8 -*- python3
""" Merge data from uff and xml observer files

Created on Mar 23 2021 15:48
@author: Aron, Luleå University of Technology
"""
import observer_xml as obsx
import observer_uff as obsu

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
    

if __name__ == '__main__':
    main()