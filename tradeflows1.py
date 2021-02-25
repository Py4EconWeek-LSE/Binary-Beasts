#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd


# In[48]:


df = pd.read_excel('servicesdataset 2.xlsx')
df


# In[87]:


cf = pd.read_excel('Gravity model categories(1).xlsx')
cf


# In[16]:


df.head(n=3)


# In[17]:


df.describe()


# In[18]:


import numpy as np

import statsmodels.api as sm
import statsmodels.formula.api as smf


# In[31]:


services = pd.read_excel('servicesdataset 2.xlsx')


# In[32]:


services.head(n=3)


# In[56]:


target = pd.read_excel('servicesdataset 2.xlsx', usecols=["trade"])


# In[91]:


#using entry cost into importer country as proxy for trade barrier
X = df[["gdp_exp","gdp_imp","dist","ent_cost_imp","smctry"]]
Y = target["trade"]
X = sm.add_constant(X)


# In[64]:


pd.isnull(services)


# In[65]:


missing_values = ["n/a", "na", "--"]
df = pd.read_excel("servicesdataset 2.xlsx", na_values = missing_values)


# In[68]:


print (df[['gdp_imp']])
print (df[['gdp_imp']].isnull())


# In[92]:


#replace na values with 0
df['gdp_exp'].fillna(0, inplace=True)
df['gdp_imp'].fillna(0, inplace=True)
df['dist'].fillna(0, inplace=True)
df['ent_cost_imp'].fillna(0, inplace=True)
df['smctry'].fillna(0, inplace=True)


# In[95]:


dummies = pd.get_dummies(cf['smctry'])


# In[93]:





# In[71]:





# In[90]:


model = sm.OLS(Y, X).fit()

print_model = model.summary()
print(print_model)


# In[ ]:




