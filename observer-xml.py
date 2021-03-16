# -*- coding: utf-8 -*- python3
""" Accelerometer data reader

Read acceleration data in xml (xmd/xme) format. Return dataframe. Save to file.

Created on Mar 16 2021 11:30
@author: Aron, Luleå University of Technology
"""
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import scipy.stats as spstats
# import pandas as pd
# import os
# import datetime as dt
import xml.etree.ElementTree as etree

import generaltools as gtol

# global variables
path_data = '../data_observer/xml/' # folder containing the raw data
path_features = '../data_observer/features_dfs/' # folder containing the features files

def main():
    filename = '1aPressT_Acc_ej-nyp_201001-210315.xme'
    full_path = path_data + filename
    tree = etree.parse(full_path)
    root = tree.getroot()
    print(root)

    # for elem in root:
    #     if elem.tag=='Node':
    #         print(elem.Node)
    #     print(elem.tag,end=' ')
    #     # print(subelem.text)

    # for child in root:
    #     print(child.tag, child.attrib)

    for nodename in root.iter('NodeName'):
        print(nodename.text)
    
    # count=0
    # for elem in root:
    #     count=count+1
    #     if count == 20:
    #         break
    #     for subelem in elem:
    #         print(subelem.tag)
            


if __name__ == '__main__':
    main()