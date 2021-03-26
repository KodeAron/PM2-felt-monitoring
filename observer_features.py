# -*- coding: utf-8 -*- python3
""" Calculate features for each 

Created on Mar 26 2021 08:20
@author: Aron, Luleå University of Technology
"""
import pandas as pd
import observer_merge as obsm

picklefilepath = obsm.picklefilepath # retrieve file location from observer_merge.py

def main():
    features()

def features():
    # calculate features for each node and strip non-interesting columns
    # delete (a)larm measurements (StorageReason=?)
    df = pd.read_pickle(picklefilepath)

    print(df.columns)

    new_dataset = df[['MeasDate','IDNode','NodeName','StorageReason','Speed','MeasValue','RawData']]

    print(new_dataset.head())

if __name__ == '__main__':
    main()