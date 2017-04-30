#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 09:34:43 2017

@author: abu
"""
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
#%%
df = pd.read_excel('Free_trial.xlsx')
#%%
df['td_main'] = pd.to_datetime(df['transaction_date'].str[0:-1].str.split('T', expand=True)[0])

df.head()
#%%
df = df[df['product']=='com.ludia.tmnt.subscription']
#%%


#%%
list(df.columns)
#%%
# Creating a period column based on the transaction_date


#%%
# Determining the user's cohort group (based on their first subscription order)
df.set_index('account_id', inplace=True)
#%%
df['CohortGroup'] = df.groupby(level=0)['td_main'].min()
df.reset_index(inplace=True)
df.head()
#%%
# Rolling up data by ChohorGroup and transaction_date
grouped = df.groupby(['CohortGroup', 'td_main'])
cohorts = grouped.agg({'account_id': pd.Series.nunique,
                       'total_amount_spent': np.sum})
cohorts.head()
#%%
cohorts.head(20)
#%%
# Labeling the CohortPeriod for each CohortGroup
def cohort_period(df):
    """
    Crearting a 'CohortPeriod' column, which is the Nth period based on the
    user's first purchase.
    
    Example
    ----------------------------
    Say you want to get the 3rd purchase for every user:
        df.sort(['account_id', 'OrderTime'] , inplace=True)
        df = df.groupby('account_id').apply(cohort_period)
        df[df.CohortPeriod==3]
        
    """
    df['CohortPeriod'] = np.arange(len(df)) + 1
    return df

cohorts = cohorts.groupby(level=0).apply(cohort_period)
cohorts.head()

#%%
# Making sure that we did all that right
x = df[(df.CohortGroup == '2017-02-01') & (df.td_main == '2017-02-01')]
y = cohorts.ix[('2017-02-01', '2017-02-01')]

#%%
# Now, use 'assert' for internal self checking and testing. 
assert(x['account_id'].nunique()== y['account_id'])


#%%
# User Retention by Cohort Group
# I want to look at the percentage change of each CohortGRoup over time but not
# the absolute change. 

# Reindex the DataFrame

cohorts.reset_index(inplace=True)
#%%
cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)
#%%
# Creating a Series holding the total size of each CohortGRoup
cohort_group_size = cohorts['account_id'].groupby(level=0).first() 

#%%
cohorts['account_id'].head()
#%%
cohorts['account_id'].unstack(0).head()
#%%
user_retention = cohorts['account_id'].unstack(0).divide(cohort_group_size, axis=1)
user_retention.head(10)
#%%
# Plotting

user_retention[['2017-02-01']].plot(figsize=(8,5))



#%%
user_retention[['2017-02-01 00:00:00']].plot(figsize=(15,12))
plt.title('Cohorts: User Retention')
plt.xticks(np.arange(1, 12.1, 1))
plt.xlim(1, 12)
plt.ylabel('% of Cohort Purchasing');
#%%

#%%
import seaborn as sns
sns.set(style = 'white')
plt.figure(figsize=(20,18))
plt.title('Cohorts: Subscription retention')
sns.heatmap(user_retention.T, mask=user_retention.T.isnull(), annot=True, fmt='.0%')
plt.show()
#%%
plt.figure(figsize=(20,18))
plt.title('Cohorts: Subscription retention')
sns.heatmap(user_retention.T, mask=user_retention.T.isnull(), annot=True)
#%%

#%%

