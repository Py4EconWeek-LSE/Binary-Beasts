#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 16:51:51 2021

@author: samuelzhu
@edits: patrickleitloff
"""

import gme as gme
import pandas as pd
import numpy as np

#loading the file
url = 'https://www.dropbox.com/s/2uha8rwc8bngcsz/servicesdataset%202.xlsx?dl=1'
df = pd.read_excel(url)

print(df.shape)
print(df.head())

df1 = pd.read_excel(url)
df1 = df1.dropna()

#drop null values from relevant columns in df 
trade_data = df[['exp','imp', 'trade', 'sector','gdp_exp', 'gdp_imp', 'distw']]
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
    print(len(unique_entries))
    return len(unique_entries) 

print(unique_count)
    
#EU countries (except for PLT)
EU = ['AUT','BEL','CYP','CZE','DNK','EST','FIN','FRA','DEU',
      'GRC','HUN','IRL','ITA','LVA','LTU','LUX','MLT','NLD',
      'POL','SVK','SVN','ESP','SWE']

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

  #bilateral accessibility, , the higher the more accessible, inversely proportional to distance      
    def BA(self, Dist, RTA):
        return (np.exp(-np.log(Dist) + 0.5*RTA))
    
  #bilateral accessibility in EU
    def BA_EU(self, EU_Dist):
        EU_Dist_array = np.array([])
        EU_BRT_array = np.array([])
        for Dist in EU_Dist.values():
            EU_Dist_array = np.append(EU_Dist_array,Dist)
        for Dist in EU_Dist_array:
            EU_BRT_array = np.append(EU_BRT_array, self.BA(Dist,1))
        return (EU_BRT_array)
        
        
#Use example of service trade between GBR (exp) and AGO (IMP) as an example
S_i = 1.70E+12
instance = Gravity(S_i) 

gravity_data = {'country' : EU, 'trade' : list(EU_trade.values()), 'GDP' : list(EU_GDP.values()), 'EU Bilateral Accessibility' : instance.BA_EU(EU_Dist)}
df_gravity = pd.DataFrame(gravity_data, columns = ['country','trade','GDP','EU Bilateral Accessibility'])
df_gravity.set_index('country',inplace=True)      

print(df_gravity)
print('GBP_GDP' +' = '+ str(S_i))


gme_data = gme.EstimationData(data_frame = df1,
                              imp_var_name = 'imp',
                              exp_var_name = 'exp',
                              trade_var_name = 'trade',
                              sector_var_name= 'sector')
print(gme_data)
gme_data.info()
gme_data.describe()


tinbergen_spec = gme.EstimationModel(estimation_data = df1,
                                lhs_var = 'trade',
                                rhs_var = ['distw','gdp_exp','gdp_imp'],
                                drop_missing = True)

tinbergen_spec.estimate()
tinbergen_spec.format_regression_table(format = "txt")

# Return a list of keys in the object
estimates.keys()
dict_keys(['all'])

# Return the result object and save it to a new variable for convenience 
results = estimates['all']
results.summary()
tinbergen_spec.ppml_diagnostics



