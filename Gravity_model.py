#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 16:51:51 2021

@author: samuelzhu
"""

import pandas as pd
import numpy as np
#loading the file
url = 'https://www.dropbox.com/s/2uha8rwc8bngcsz/servicesdataset%202.xlsx?dl=1'
df = pd.read_excel(url)
print(df.shape)
print(df.head())

#drop null values from relevant columns in df 
trade_data = df[['exp','imp', 'trade', 'gdp_exp', 'gdp_imp', 'distw']]
trade_data = trade_data.dropna()


#count number of unique exp countries and sectors
exp_countries = df['exp'].tolist()
sector = df['sector'].tolist()

#count unique countries and sectors
def unique_count (column):
    unique_entries = []
    for e in column:
        if e not in unique_entries:
            unique_entries.append(e)
    print(unique_entries)
    return len(unique_entries) 
    

print (unique_count(exp_countries))
print (unique_count(sector))
print (trade_data)

       
        
        
        
    

