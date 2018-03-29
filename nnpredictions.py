# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 22:59:00 2018

@author: Vince
"""
import pandas as pd
import numpy as np


from keras.models import Sequential
from keras.layers.core import Dense

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

df = pd.read_csv('data.csv')

#print(df['name'].value_counts())

df = df[df['cluster'] == 9]
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

X = df.drop(['filename','Unnamed: 0','street reached','name','cluster',
       'hand','board','hand strength fl','hand strength tr','hand strength rv',
       'hand strength ^2','bluff flop','bluff turn',
       'bluff river'], axis = 1)
#X = df[['log tot bets','log tot bets/stack','log tot agg',
#       'tot bets/stack','tot bets','rv bets(bb)','rv bets/pot',
#       'fl bets(bb)','fl bets/pot','tot agg','tr bets(bb)',
#       'tr bets/pot']]
y = df['hand strength ^2']
print(X.columns)
#print(y)
X_train, X_test, y_train, y_test = train_test_split(X,y)
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)
print(X.shape)
model = Sequential()
model.add(Dense(50, input_dim = 38, activation = 'sigmoid'))
model.add(Dense(50, activation = 'sigmoid'))

model.add(Dense(1))

model.compile(loss = 'mean_squared_error', optimizer = 'adam')

history = model.fit(X_train, y_train, validation_data = (X_test, y_test), epochs = 20)

ax2 = sns.heatmap(df.corr())
ax = df2.plot.scatter(x = 'hand strength ^2', y = 'log tot bets/stack', color = 'red')
df.plot.scatter(x = 'hand strength ^2', y = 'log tot bets/stack', color = 'blue', ax = ax)

plt.figure(figsize = (10,10))
plt.plot(history.history['loss'], label = 'Training Loss')
plt.plot(history.history['val_loss'], label = 'Test Loss')
plt.legend()

z = pd.DataFrame(model.predict(X_test))
z['test actual'] = list(y_test)

z[0] = np.sqrt(z[0])
z['test actual'] = np.sqrt(z['test actual'])
z['diff'] = z[0] - z['test actual']
print(np.mean(np.abs(z['diff'])))
print(z.sort_values('diff').values)
print(z)

print("std", np.std(z['diff']))
print("median", np.median(np.abs(z['diff'])))
plt.figure(figsize = (7,7))
z['diff'].plot.hist()
#print(np.std(z['diff']))
