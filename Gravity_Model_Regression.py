#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 16:07:52 2021

@author: samuelzhu
"""

import pandas as pd
import numpy as np
import gme as gme
#loading the file and inspect data
url = 'https://www.dropbox.com/s/2uha8rwc8bngcsz/servicesdataset%202.xlsx?dl=1'
df = pd.read_excel(url)
print(df.shape)
print(df.head())


#drop null values from relevant columns in df 
trade_data = df[['exp','imp', 'trade', 'year','gdp_exp', 'gdp_imp', 'contig','comlang_off','distw','ent_cost_imp', 'ent_cost_exp', 'colony']]
trade_data = trade_data.dropna()


#include the accessibility column
trade_data['bilateral accessibility'] = np.exp(-np.log(trade_data['distw']))


#create EU dummy column
EU = ['AUT','BEL','CYP','CZE','DNK','EST','FIN','FRA','DEU','GRC','HUN','IRL','ITA','LVA','LTU','LUX','MLT','NLD','POL','SVK','SVN','ESP','SWE','GBR']
imp_EU = {}
exp_EU = {}
imp_countries = trade_data['imp'].tolist()
exp_countries = trade_data['exp'].tolist()
for country in imp_countries:
    if country in EU:
        imp_EU[country] = 1
        exp_EU[country] = 1
    else:
        imp_EU[country] = 0
        exp_EU[country] = 0
trade_data['imp_is_EU'] = trade_data['imp'].map(imp_EU)
trade_data['exp_is_EU'] = trade_data['exp'].map(exp_EU)
trade_data['between_EU'] = trade_data['imp_is_EU']*trade_data['exp_is_EU']
        
#include log GDP and log distance  
trade_data['log_gdp_exp'] = np.log(trade_data['gdp_exp'])
trade_data['log_gdp_imp'] = np.log(trade_data['gdp_imp'])
trade_data['log_distance'] = np.log(trade_data['distw'])
print(trade_data.head())

#data for estimation
gme_data = gme.EstimationData(data_frame=trade_data,
                              imp_var_name='imp',
                              exp_var_name='exp',
                              trade_var_name='trade',
                              year_var_name='year')

#basic regression data
model_basic = gme.EstimationModel(estimation_data = gme_data,
                                         lhs_var = 'trade',
                                         rhs_var = ['log_gdp_exp',
                                                    'log_gdp_imp',
                                                    'log_distance',
                                                    'comlang_off',
                                                    'contig'
                                                    ])
basic_estimates = model_basic.estimate()


# Return the result object and save it to a new variable for convenience 
results = basic_estimates['all']
print(results.summary())

#export trade_data to excel:
trade_data.to_excel('trade_data.xlsx')
trade_data.to_csv('trade_data.csv')


#regression using colonial history as IV
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.gmm import IV2SLS  

Instrument = trade_data[['colony']]
end = trade_data[['trade']]
exo = trade_data[['log_gdp_exp']]

resultIV = IV2SLS(end, exo, Instrument).fit()


print(resultIV.summary())

#impact of EU membership on trade size

#Including dummy EU variable in basic regression model

model_EU_dummy = gme.EstimationModel(estimation_data = gme_data,
                                         lhs_var = 'trade',
                                         rhs_var = ['log_gdp_exp',
                                                    'log_gdp_imp',
                                                    'log_distance',
                                                    'comlang_off',
                                                    'contig','between_EU'
                                                    ])
EU_dummy_estimates = model_EU_dummy.estimate()

result_EU_dummy = EU_dummy_estimates['all']
print(result_EU_dummy.summary())



