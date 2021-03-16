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
            
def nodelist(xmefilename):
    full_path = path_data + xmefilename
    tree = etree.parse(full_path)
    root = tree.getroot()

    nodelist = []
    list_of_parents = []

    for node in root.findall('Node'):
        IDNode = node.find('IDNode')
        IDParent = node.find('IDParent')
        NodeName = node.find('NodeName')

        # add to list, as dictionary
        nodedict = {'IDNode':IDNode.text, 'IDParent':IDParent.text, 'NodeName':NodeName.text}
        nodelist.append(nodedict)

        # save IDParents in list
        list_of_parents.append(IDParent.text)

    # delete all parent nodes, all nodes except those in the "bottom"
    iteration=0
    while iteration < len(nodelist):
        if nodelist[iteration]['IDNode'] in list_of_parents:
            nodelist.pop(iteration)
        else:
            iteration=iteration+1            

    return nodelist

if __name__ == '__main__':
    main()