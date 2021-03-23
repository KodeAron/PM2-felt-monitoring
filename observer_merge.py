# -*- coding: utf-8 -*- python3
""" Merge data from uff and xml observer files

Created on Mar 23 2021 15:48
@author: Aron, Luleå University of Technology
"""
# import observer-xml as obsx
# import observer-uff as obsu

def main():
    save_raw_data()

def save_raw_data():
    """ Save a dataframe with raw data
    Use pickle to save raw data in dataframe.
    """
    nodelist = obsx.nodelist()
    print(nodelist

if __name__ == '__main__':
    main()