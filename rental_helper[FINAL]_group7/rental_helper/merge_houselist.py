# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 19:07:36 2021

@author: Lenovo

@description: merge two houselist source together
"""

import pandas as pd

def merge_list():
    f1 = pd.read_csv('backupcsv\rental_listings.csv', encoding = 'utf-8')
    f2 = pd.read_csv('backupcsv\domain.csv', encoding = 'utf-8')

    file = [f1, f2]
    output = pd.concat(file, sort=False)
    output.to_csv('backupcsv\rental_listing.csv', index=0, sep=',', encoding = 'utf_8_sig')

if __name__ == 'main':
    merge_list()