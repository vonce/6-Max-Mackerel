# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

stats = pd.read_csv('clusteredstats.csv')
data = pd.read_csv('data.csv')

clusterlist = []

stats = stats.drop(['Unnamed: 0'], axis = 1)
stats = stats.rename(columns = {'Unnamed: 0.1': 'name'})
data = data.drop(['Unnamed: 0'], axis = 1)
pd.set_option('display.max_columns', None)

print(stats.groupby('cluster').count())
print(stats.groupby('cluster').mean())

#print(stats.head())
#print(data.head())

#print(stats[stats['cluster'] == 1])
i = 0
for name in data['name']:
    i = i + 1
    if i % 1000 == 0:
        print(i, 'of', len(data['name']))
    #print(stats.loc[stats['name'] == name, 'cluster'].values[0])
    clusterlist.append(stats.loc[stats['name'] == name, 'cluster'].values[0])
    
data['cluster'] = clusterlist

data.to_csv('data.csv')