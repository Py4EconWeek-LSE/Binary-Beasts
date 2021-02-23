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


#make the index country name
df.set_index('imp',inplace=True)

#count number of unique sectors
sector = df['sector'].tolist()

#count unique countries and sectors
def unique_count (column):
    unique_entries = []
    for e in column:
        if e not in unique_entries:
            unique_entries.append(e)
    print(unique_entries)
    return len(unique_entries) 

    
#EU countries (except for PLT)
EU = ['AUT','BEL','CYP','CZE','DNK','EST','FIN','FRA','DEU','GRC','HUN','IRL','ITA','LVA','LTU','LUX','MLT','NLD','POL','SVK','SVN','ESP','SWE']

#GDP of EU countries
EU_GDP = {}
for country in EU:
    if country not in EU_GDP:
       EU_GDP[country] = int(df.loc[country,'gdp_imp'].unique())


#Distance and trade between EU countries and UK
df = df.reset_index()
df.set_index('exp',inplace=True)
df_GBR = df.loc[['GBR']]
df_GBR = df_GBR.reset_index()
df_GBR.set_index('imp',inplace=True)
EU_Dist = {}
EU_trade = {}
for country in EU:
    if country not in EU_Dist:
       EU_Dist[country] = float(df_GBR.loc[country,'distwces'].unique())
for country in EU:
    if country not in EU_trade:
       EU_trade[country] = df_GBR.loc[country,'trade'].unique() 
for keys, values in EU_trade.items():
    EU_trade[keys] = sum(values)
    

#the Gravity Model
class Gravity:

    def __init__(self, S_i):
        self.S_i = S_i

  #bilateral resistance term      
    def BRT(self, Dist, RTA):
        return (np.exp(-np.log(Dist) + 0.5*RTA))
    
  #multilateral resistance term
    def MRT(self, EU_Dist):
        EU_Dist_array = np.array([])
        EU_BRT_array = np.array([])
        for Dist in EU_Dist.values():
            EU_Dist_array = np.append(EU_Dist_array,Dist)
        for Dist in EU_Dist_array:
            EU_BRT_array = np.append(EU_BRT_array, self.BRT(Dist,1))
        return (EU_BRT_array)
        
        
#Use example of service trade between GBR (exp) and AGO (IMP) as an example
S_i = 1.70E+12
instance = Gravity(S_i) 

vgravity_data = {'country' : EU, 'trade' : list(EU_trade.values()), 'GDP' : list(EU_GDP.values()), 'MRT' : instance.MRT(EU_Dist)}
df_gravity = pd.DataFrame(gravity_data, columns = ['country','trade','GDP','MRT'])
df_gravity.set_index('country',inplace=True)      

print(df_gravity)
print('GBP_GDP' +' = '+ str(S_i))

