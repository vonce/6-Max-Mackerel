#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 14:21:22 2018

@author: Vince
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, FunctionTransformer, Imputer
import matplotlib.pyplot as plt

print(df)
df['hand strength ^4'] = df['hand strength'] ** 4
df['log tot bets'] = np.log(df['tot bets'])
#print(df.corr()['hand strength ^4'].sort_values())

#print((df['hand strength ^4']).plot.hist())
#print((df.plot.scatter(x = 'tot bets', y = 'hand strength ^4')))
#print((np.log(df['tot bets'])).plot.hist())

X = df.drop(['name','hand','board','hand strength','hand strength ^4'], axis = 1)
y = df['hand strength ^4']
print(X.columns)
print(y)
X_train, X_test, y_train, y_test = train_test_split(X,y)
ss = StandardScaler()
lasso = Lasso()

pipe = Pipeline([
    ('ss', ss),
    ('lasso', lasso)
])
params = {
        'lasso__alpha': np.arange(.01,.05,.25)
}
gs = GridSearchCV(pipe, param_grid = params)
gs.fit(X_train, y_train)

print(gs.best_score_)
print(gs.best_params_)
print(gs.score(X_test, y_test))