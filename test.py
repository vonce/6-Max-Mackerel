#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 14:21:22 2018

@author: Vince
"""
import pandas as pd
import numpy as np
import handrank as hr
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, FunctionTransformer, Imputer
import matplotlib.pyplot as plt
df = pd.read_csv('data.csv')

#print(df['name'].value_counts())
print(df['board'].dtypes)
#df['board texture'] = df['board'].apply(hr.boardtexture)
df['hand strength ^2'] = df['hand strength rv'] ** 2
df['tot bets/stack'] = df['tot bets']/df['pf stack(bb)']
df['log tot bets'] = np.log(df['tot bets'])
df['log tot bets/stack'] = np.log(df['tot bets/stack'])
df['log tot agg'] = np.sqrt(df['tot agg'])
#df['pf agg'] = np.sqrt(df['pf agg'])
#df['rv agg'] = np.sqrt(df['rv agg'])
#df['tr agg'] = np.sqrt(df['tr agg'])
#df['fl agg'] = np.sqrt(df['fl agg'])
#df['rv bets(bb)'] = np.sqrt(df['rv bets(bb)'])
#df['tr bets(bb)'] = np.sqrt(df['tr bets(bb)'])
#df['fl bets(bb)'] = np.sqrt(df['fl bets(bb)'])
#df['pf bets(bb)'] = np.sqrt(df['pf bets(bb)'])
#df['rv bets/pot'] = np.sqrt(df['rv bets/pot'])
#df['tr bets/pot'] = np.sqrt(df['tr bets/pot'])
#df['fl bets/pot'] = np.sqrt(df['fl bets/pot'])

#print(df[df['hand strength ^2'] == 0])
print(df.columns)
df2 = df
df2 = df2[df2['street reached'] == 3]
df = df.dropna(axis = 0)
df = df[df['bluff river'] == 0]
df = df[df['bluff turn'] == 0]
#df = df[df['bluff flop'] == 0]
df = df[df['street reached'] == 3]
#df = df[df['pf stack(bb)'] > 80]
#df = df[df['straight draws flop'] == 0]
#df = df[df['flush draws flop'] == 0]
#df = df[df['straight draws turn'] == 0]
#df = df[df['flush draws turn'] == 0]
#print(df['bluff river'].value_counts())
print(df.corr()['hand strength ^2'].sort_values())
print(df[df['hand strength rv'].isnull()]['hand strength rv'])
df['hand strength ^2'].plot.hist()
#df['log tot bets'].plot.hist()
ax = df2.plot.scatter(x = 'hand strength ^2', y = 'log tot bets', color = 'red')
df.plot.scatter(x = 'hand strength ^2', y = 'log tot bets', color = 'blue', ax = ax)

#X = df.drop(['filename','Unnamed: 0','street reached','name',
#       'hand','board','hand strength fl','hand strength tr','hand strength rv',
#       'hand strength ^2','bluff flop','bluff turn',
#       'bluff river'], axis = 1)
X = df[['log tot bets','log tot bets/stack','log tot agg',
       'tot bets/stack','tot bets','rv bets(bb)','rv bets/pot',
       'fl bets(bb)','fl bets/pot','tot agg','tr bets(bb)',
       'tr bets/pot']]
y = df['hand strength ^2']
#print(X.columns)
#print(y)
X_train, X_test, y_train, y_test = train_test_split(X,y)
ss = StandardScaler()
gbr = GradientBoostingRegressor()
rfr = RandomForestRegressor()
pipe = Pipeline([
    ('ss', ss),
    ('rfr', rfr)
])
params = {
        
}
gs = GridSearchCV(pipe, param_grid = params)
gs.fit(X_train, y_train)

print(gs.best_score_)
print(gs.best_params_)
print(gs.score(X_test, y_test))

z = pd.DataFrame(gs.predict(X_test))
z['test actual'] = list(y_test)

#z[0] = np.sqrt(z[0])
#z['test actual'] = np.sqrt(z['test actual'])
z['diff'] = z[0] - z['test actual']
print(np.median(np.abs(z['diff'])))
print(z)
#z['diff'].plot.hist()
print(np.std(z['diff']))