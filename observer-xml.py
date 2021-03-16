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
    filename = '1aPressT_Acc_ej-nyp_201001-210315'
    xme_file = filename + '.xme'
    xmd_file = filename + '.xmd'
    list_of_nodes = nodelist(xme_file)
    print(list_of_nodes)

    # for elem in root:
    #     if elem.tag=='Node':
    #         print(elem.Node)
    #     print(elem.tag,end=' ')
    #     # print(subelem.text)

    # for child in root:
    #     print(child.tag, child.attrib)
    
    # count=0
    # for elem in root:
    #     count=count+1
    #     if count == 20:
    #         break
    #     for subelem in elem:
    #         print(subelem.tag)
            
def nodelist(xmefilename):
    full_path = path_data + xmefilename
    tree = etree.parse(full_path)
    root = tree.getroot()

    nodelist = []

    for node in root.findall('Node'):
        # for elem in node:
        IDNode = node.find('IDNode')
        print('IDNode : ' + IDNode.text)
        IDParent = node.find('IDParent')
        print('IDParent : ' + IDParent.text)
        NodeName = node.find('NodeName')
        print('NodeName : ' + NodeName.text)

        # add to list, as dictionary
        nodedict = {'IDNode':IDNode.text, 'IDParent':IDParent.text, 'NodeName':NodeName.text}
        nodelist.append(nodedict)

    return nodelist

if __name__ == '__main__':
    main()