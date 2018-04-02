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
import seaborn as sns

def nnmodel():
    global probdensitypf
    global modelpf
    global probdensityfl
    global probdensityefffl
    global modelfl
    global modelefffl
    global probdensitytr
    global probdensityefftr
    global modeltr
    global modelefftr
    global probdensityrv
    global modelrv
    
    data = pd.read_csv('data.csv')
    stats = pd.read_csv('stats.csv')
    print(data.columns)
    data['hand strength fl ^2'] = data['hand strength fl'] ** 2
    data['hand strength tr ^2'] = data['hand strength tr'] ** 2
    data['hand strength rv ^2'] = data['hand strength rv'] ** 2
    data['eff hand strength fl ^2'] = data['eff hand strength fl'] ** 2
    data['eff hand strength tr ^2'] = data['eff hand strength tr'] ** 2
    data['tot bets pf/stack'] = data['pf bets(bb)']/data['pf stack(bb)']
    data['log tot bets pf'] = np.log(data['pf bets(bb)'])
    data['log tot bets pf/stack'] = np.log(data['tot bets pf/stack'])
    data['log tot agg pf'] = np.sqrt(data['pf agg'])
    data['tot bets fl/stack'] = data['total bets flop']/data['pf stack(bb)']
    data['log tot bets fl'] = np.log(data['total bets flop'])
    data['log tot bets fl/stack'] = np.log(data['tot bets fl/stack'])
    data['log tot agg fl'] = np.sqrt(data['fl agg'])
    data['tot bets tr/stack'] = data['total bets turn']/data['pf stack(bb)']
    data['log tot bets tr'] = np.log(data['total bets turn'])
    data['log tot bets tr/stack'] = np.log(data['tot bets tr/stack'])
    data['log tot agg tr'] = np.sqrt(data['tr agg'])
    data['tot bets/stack'] = data['tot bets']/data['pf stack(bb)']
    data['log tot bets'] = np.log(data['tot bets'])
    data['log tot bets/stack'] = np.log(data['tot bets/stack'])
    data['log tot agg'] = np.sqrt(data['tot agg'])
    stats = stats.drop(['avgstack', 'net', 
                'numraisedpf', 'numreraisedpf',
                'numraisedfl', 'numreraisedfl', 'numplayedfl', 'foldtoreraisefl',
                'numraisedtr', 'numreraisedtr', 'numplayedtr', 'foldtoreraisetr',
                'numraisedrv', 'numreraisedrv', 'numplayedrv', 'foldtoreraiserv',
                'numplayedsd',
                'bb/100hands', 'winpercent'], axis = 1)
    data = data.merge(stats, left_on='name', right_on='Unnamed: 0',how='inner')
    data = data.drop('numplayedpf',axis = 1)
    ###########
    datapf = data[['pf stack(bb)','#pl pf','position pf','position pf/#pl pf','pf bets(bb)','pf agg','stack/pfpot',
                   'tot bets pf/stack','log tot bets pf','log tot bets pf/stack','log tot agg pf',
                   'foldpf', 'callpf','raisepf', 'foldtoraisepf', 'reraisepf', 'foldtoreraisepf', 'pctseenfl',
                   'foldfl', 'callfl', 'betfl', 'raisefl', 'foldtoraisefl', 'reraisefl',
                   'pctseentr', 'foldtr', 'calltr', 'bettr', 'raisetr', 'foldtoraisetr',
                   'reraisetr', 'pctseenrv', 'foldrv', 'callrv', 'betrv', 'raiserv',
                   'foldtoraiserv', 'reraiserv', 'pctseensd']]
    X_train, X_test, y_train, y_test = train_test_split(datapf,data['hand strength pf'])
    sshandstrengthpf = StandardScaler()
    X_train = sshandstrengthpf.fit_transform(X_train)
    X_test = sshandstrengthpf.transform(X_test)
    modelpf = Sequential()
    modelpf.add(Dense(50, input_dim = 39, activation = 'sigmoid'))
    modelpf.add(Dense(25, activation = 'sigmoid'))
    modelpf.add(Dense(1))
    modelpf.compile(loss = 'mean_squared_error', optimizer = 'adam')
    history = modelpf.fit(X_train, y_train, validation_data = (X_test, y_test), epochs = 25)
    probdensitypf = pd.DataFrame(modelpf.predict(datapf))
    probdensitypf['test actual'] = list(data['hand strength pf'])
    probdensitypf['diff'] = probdensitypf[0] - probdensitypf['test actual']
    print("preflop fitting complete")
    ############pf
    data['predicted pf'] = modelpf.predict(datapf)
    datafl = data[data['street reached'] >= 1]
    datafl = datafl[datafl['bluff flop'] == 0]
    datafl = datafl[['pf stack(bb)','#pl pf','position pf','position pf/#pl pf','pf bets(bb)','pf agg','stack/pfpot',
                     'tot bets pf/stack', 'log tot bets pf', 'log tot bets pf/stack', 'log tot agg pf',
                   'board texture flop','fl stack(bb)', '#pl fl',
                   'position fl', 'position fl/#pl fl', 'fl bets(bb)', 'fl bets/pot',
                   'fl agg', 'stack/flpot', 'total bets flop','tot bets fl/stack',
                   'log tot bets fl','log tot bets fl/stack',
                   'foldpf', 'callpf','raisepf', 'foldtoraisepf', 'reraisepf', 'foldtoreraisepf', 'pctseenfl',
                   'foldfl', 'callfl', 'betfl', 'raisefl', 'foldtoraisefl', 'reraisefl',
                   'pctseentr', 'foldtr', 'calltr', 'bettr', 'raisetr', 'foldtoraisetr',
                   'reraisetr', 'pctseenrv', 'foldrv', 'callrv', 'betrv', 'raiserv',
                   'foldtoraiserv', 'reraiserv', 'pctseensd','hand strength fl ^2','eff hand strength fl ^2','predicted pf']]

    X_train, X_test, y_train, y_test = train_test_split(datafl.drop(['hand strength fl ^2','eff hand strength fl ^2'], axis = 1),datafl['hand strength fl ^2'])
    sshandstrengthfl = StandardScaler()
    X_train = sshandstrengthfl.fit_transform(X_train)
    X_test = sshandstrengthfl.transform(X_test)
    modelfl = Sequential()
    modelfl.add(Dense(50, input_dim = 53, activation = 'sigmoid'))
    modelfl.add(Dense(25, activation = 'sigmoid'))
    modelfl.add(Dense(1))
    modelfl.compile(loss = 'mean_squared_error', optimizer = 'adam')
    history = modelfl.fit(X_train, y_train, validation_data = (X_test, y_test), epochs = 25)
    probdensityfl = pd.DataFrame(modelfl.predict(datafl.drop(['hand strength fl ^2','eff hand strength fl ^2'], axis = 1)))
    probdensityfl['test actual'] = list(datafl['hand strength fl ^2'])
    probdensityfl[0] = np.sqrt(probdensityfl[0])
    probdensityfl['test actual'] = np.sqrt(probdensityfl['test actual'])
    probdensityfl['diff'] = probdensityfl[0] - probdensityfl['test actual']

    X_train, X_test, y_train, y_test = train_test_split(datafl.drop(['hand strength fl ^2','eff hand strength fl ^2'], axis = 1),datafl['eff hand strength fl ^2'])
    sshandstrengthefffl = StandardScaler()
    X_train = sshandstrengthefffl.fit_transform(X_train)
    X_test = sshandstrengthefffl.transform(X_test)
    modelefffl = Sequential()
    modelefffl.add(Dense(50, input_dim = 53, activation = 'sigmoid'))
    modelefffl.add(Dense(25, activation = 'sigmoid'))
    modelefffl.add(Dense(1))
    modelefffl.compile(loss = 'mean_squared_error', optimizer = 'adam')
    history = modelefffl.fit(X_train, y_train, validation_data = (X_test, y_test), epochs = 25)
    probdensityefffl = pd.DataFrame(modelefffl.predict(datafl.drop(['hand strength fl ^2','eff hand strength fl ^2'], axis = 1)))
    probdensityefffl['test actual'] = list(datafl['eff hand strength fl ^2'])
    probdensityefffl[0] = np.sqrt(probdensityefffl[0])
    probdensityefffl['test actual'] = np.sqrt(probdensityefffl['test actual'])
    probdensityefffl['diff'] = probdensityefffl[0] - probdensityefffl['test actual']
    print("flop fitting complete")
    ############fl
    datatr = data[data['street reached'] >= 1]
    datatr = datatr[datatr['bluff flop'] == 0]
    datatr['predicted fl'] = modelfl.predict(datafl.drop(['hand strength fl ^2','eff hand strength fl ^2'], axis = 1))
    datatr['predicted eff fl'] = modelefffl.predict(datafl.drop(['hand strength fl ^2','eff hand strength fl ^2'], axis = 1))
    datatr = datatr[datatr['street reached'] >= 2]
    datatr = datatr[datatr['bluff turn'] == 0]
    datatr = datatr[['pf stack(bb)','#pl pf','position pf','position pf/#pl pf','pf bets(bb)','pf agg','stack/pfpot',
                     'tot bets pf/stack', 'log tot bets pf', 'log tot bets pf/stack', 'log tot agg pf',
                   'board texture flop','fl stack(bb)', '#pl fl',
                   'position fl', 'position fl/#pl fl', 'fl bets(bb)', 'fl bets/pot',
                   'fl agg', 'stack/flpot', 'total bets flop','tot bets fl/stack',
                   'log tot bets fl','log tot bets fl/stack',
                   'board texture turn','tr stack(bb)', '#pl tr',
                   'position tr', 'position tr/#pl tr', 'tr bets(bb)', 'tr bets/pot',
                   'tr agg', 'stack/trpot', 'total bets turn','tot bets tr/stack',
                   'log tot bets tr','log tot bets tr/stack','log tot bets/stack',
                   'foldpf', 'callpf','raisepf', 'foldtoraisepf', 'reraisepf', 'foldtoreraisepf', 'pctseenfl',
                   'foldfl', 'callfl', 'betfl', 'raisefl', 'foldtoraisefl', 'reraisefl',
                   'pctseentr', 'foldtr', 'calltr', 'bettr', 'raisetr', 'foldtoraisetr',
                   'reraisetr', 'pctseenrv', 'foldrv', 'callrv', 'betrv', 'raiserv',
                   'foldtoraiserv', 'reraiserv', 'pctseensd','hand strength tr ^2','eff hand strength tr ^2',
                   'predicted pf','predicted fl','predicted eff fl']]
    
    X_train, X_test, y_train, y_test = train_test_split(datatr.drop(['hand strength tr ^2','eff hand strength tr ^2'], axis = 1),datatr['hand strength tr ^2'])
    sshandstrengthtr = StandardScaler()
    X_train = sshandstrengthtr.fit_transform(X_train)
    X_test = sshandstrengthtr.transform(X_test)
    modeltr = Sequential()
    modeltr.add(Dense(50, input_dim = 69, activation = 'sigmoid'))
    modeltr.add(Dense(25, activation = 'sigmoid'))
    modeltr.add(Dense(1))
    modeltr.compile(loss = 'mean_squared_error', optimizer = 'adam')
    history = modeltr.fit(X_train, y_train, validation_data = (X_test, y_test), epochs = 25)
    probdensitytr = pd.DataFrame(modeltr.predict(datatr.drop(['hand strength tr ^2','eff hand strength tr ^2'], axis = 1)))
    probdensitytr['test actual'] = list(datatr['hand strength tr ^2'])
    probdensitytr[0] = np.sqrt(probdensitytr[0])
    probdensitytr['test actual'] = np.sqrt(probdensitytr['test actual'])
    probdensitytr['diff'] = probdensitytr[0] - probdensitytr['test actual']

    X_train, X_test, y_train, y_test = train_test_split(datatr.drop(['hand strength tr ^2','eff hand strength tr ^2'], axis = 1),datatr['eff hand strength tr ^2'])
    sshandstrengthefftr = StandardScaler()
    X_train = sshandstrengthefftr.fit_transform(X_train)
    X_test = sshandstrengthefftr.transform(X_test)
    modelefftr = Sequential()
    modelefftr.add(Dense(50, input_dim = 69, activation = 'sigmoid'))
    modelefftr.add(Dense(25, activation = 'sigmoid'))
    modelefftr.add(Dense(1))
    modelefftr.compile(loss = 'mean_squared_error', optimizer = 'adam')
    history = modelefftr.fit(X_train, y_train, validation_data = (X_test, y_test), epochs = 25)
    probdensityefftr = pd.DataFrame(modelefftr.predict(datatr.drop(['hand strength tr ^2','eff hand strength tr ^2'], axis = 1)))
    probdensityefftr['test actual'] = list(datatr['eff hand strength tr ^2'])
    probdensityefftr[0] = np.sqrt(probdensityefftr[0])
    probdensityefftr['test actual'] = np.sqrt(probdensityefftr['test actual'])
    probdensityefftr['diff'] = probdensityefftr[0] - probdensityefftr['test actual']
    print("turn fitting complete")
    #########tr
    datarv = data[data['street reached'] >= 1]
    datarv = datarv[datarv['bluff flop'] == 0]
    datarv['predicted fl'] = modelfl.predict(datafl.drop(['hand strength fl ^2','eff hand strength fl ^2'], axis = 1))
    datarv['predicted eff fl'] = modelefffl.predict(datafl.drop(['hand strength fl ^2','eff hand strength fl ^2'], axis = 1))
    datarv = datarv[datarv['street reached'] >= 2]
    datarv = datarv[datarv['bluff turn'] == 0]
    datarv['predicted tr'] = modeltr.predict(datatr.drop(['hand strength tr ^2','eff hand strength tr ^2'], axis = 1))
    datarv['predicted eff tr'] = modelefftr.predict(datatr.drop(['hand strength tr ^2','eff hand strength tr ^2'], axis = 1))
    datarv = datarv[datarv['street reached'] >= 3]
    datarv = datarv[datarv['bluff river'] == 0]
    datarv = datarv[['pf stack(bb)','#pl pf','position pf','position pf/#pl pf','pf bets(bb)','pf agg','stack/pfpot',
                     'tot bets pf/stack', 'log tot bets pf', 'log tot bets pf/stack', 'log tot agg pf',
                   'board texture flop','fl stack(bb)', '#pl fl',
                   'position fl', 'position fl/#pl fl', 'fl bets(bb)', 'fl bets/pot',
                   'fl agg', 'stack/flpot', 'total bets flop','tot bets fl/stack',
                   'log tot bets fl','log tot bets fl/stack',
                   'board texture turn','tr stack(bb)', '#pl tr',
                   'position tr', 'position tr/#pl tr', 'tr bets(bb)', 'tr bets/pot',
                   'tr agg', 'stack/trpot', 'total bets turn','tot bets tr/stack',
                   'log tot bets tr','log tot bets tr/stack',
                   'rv stack(bb)', '#pl rv', 'position rv','position rv/#pl rv', 'rv bets(bb)', 'rv bets/pot', 'rv agg',
                   'stack/rvpot','tot bets', 'tot agg',
                   'tot bets/stack','log tot bets','log tot bets/stack','log tot agg',
                   'foldpf', 'callpf','raisepf', 'foldtoraisepf', 'reraisepf', 'foldtoreraisepf', 'pctseenfl',
                   'foldfl', 'callfl', 'betfl', 'raisefl', 'foldtoraisefl', 'reraisefl',
                   'pctseentr', 'foldtr', 'calltr', 'bettr', 'raisetr', 'foldtoraisetr',
                   'reraisetr', 'pctseenrv', 'foldrv', 'callrv', 'betrv', 'raiserv',
                   'foldtoraiserv', 'reraiserv', 'pctseensd','hand strength rv ^2',
                   'predicted pf','predicted fl','predicted eff fl']]
    
    X_train, X_test, y_train, y_test = train_test_split(datarv.drop('hand strength rv ^2', axis = 1),datarv['hand strength rv ^2'])
    sshandstrengthrv = StandardScaler()
    X_train = sshandstrengthrv.fit_transform(X_train)
    X_test = sshandstrengthrv.transform(X_test)
    modelrv = Sequential()
    modelrv.add(Dense(50, input_dim = 82, activation = 'sigmoid'))
    modelrv.add(Dense(25, activation = 'sigmoid'))
    modelrv.add(Dense(1))
    modelrv.compile(loss = 'mean_squared_error', optimizer = 'adam')
    history = modelrv.fit(X_train, y_train, validation_data = (X_test, y_test), epochs = 25)
    probdensityrv = pd.DataFrame(modelrv.predict(datarv.drop('hand strength rv ^2', axis = 1)))
    probdensityrv['test actual'] = list(datarv['hand strength rv ^2'])
    probdensityrv[0] = np.sqrt(probdensityrv[0])
    probdensityrv['test actual'] = np.sqrt(probdensityrv['test actual'])
    probdensityrv['diff'] = probdensityrv[0] - probdensityrv['test actual']
    #########rv
    print("pf std", np.std(probdensitypf['diff']))
    print("fl std", np.std(probdensityfl['diff']))
    print("eff fl std", np.std(probdensityefffl['diff']))
    print("tr std", np.std(probdensitytr['diff']))
    print("eff tr std", np.std(probdensityefftr['diff']))
    print("rv std", np.std(probdensityrv['diff']))
    print("river fitting complete")

def nnmodelpredictpf(pfinput, pfhandperc):
    plt.figure();
    a = probdensitypf[(probdensitypf[0] > max(probdensitypf[0])-.05) & (probdensitypf[0] < max(probdensitypf[0])+.05)]['test actual'].plot.hist()
    plt.figure();
    b = probdensitypf[(probdensitypf[0] > min(probdensitypf[0])-.05) & (probdensitypf[0] < min(probdensitypf[0])+.05)]['test actual'].plot.hist()

def nnmodelpredictfl(flinput, flhandperc):
    plt.figure();
    c = probdensityfl[(probdensityfl[0] > max(probdensityfl[0])-.05) & (probdensityfl[0] < max(probdensityfl[0])+.05)]['test actual'].plot.hist()
    plt.figure();
    d = probdensityfl[(probdensityfl[0] > min(probdensityfl[0])-.05) & (probdensityfl[0] < min(probdensityfl[0])+.05)]['test actual'].plot.hist()

def nnmodelpredictefffl(flinput, effflhandperc):
    plt.figure();
    e = probdensityefffl[(probdensityefffl[0] > max(probdensityefffl[0])-.05) & (probdensityefffl[0] < max(probdensityefffl[0])+.05)]['test actual'].plot.hist()
    plt.figure();
    f = probdensityefffl[(probdensityefffl[0] > min(probdensityefffl[0])-.05) & (probdensityefffl[0] < min(probdensityefffl[0])+.05)]['test actual'].plot.hist()

def nnmodelpredicttr(trinput, trhandperc):
    plt.figure();
    g = probdensitytr[(probdensitytr[0] > max(probdensitytr[0])-.05) & (probdensitytr[0] < max(probdensitytr[0])+.05)]['test actual'].plot.hist()
    plt.figure();
    h = probdensitytr[(probdensitytr[0] > min(probdensitytr[0])-.05) & (probdensitytr[0] < min(probdensitytr[0])+.05)]['test actual'].plot.hist()

def nnmodelpredictefftr(trinput, trhandperc):
    plt.figure();
    i = probdensityefftr[(probdensityefftr[0] > max(probdensityefftr[0])-.05) & (probdensityefftr[0] < max(probdensityefftr[0])+.05)]['test actual'].plot.hist()
    plt.figure();
    j = probdensityefftr[(probdensityefftr[0] > min(probdensityefftr[0])-.05) & (probdensityefftr[0] < min(probdensityefftr[0])+.05)]['test actual'].plot.hist()

def nnmodelpredictrv(rvinput, rvhandperc):
    plt.figure();
    k = probdensityrv[(probdensityrv[0] > max(probdensityrv[0])-.05) & (probdensityrv[0] < max(probdensityrv[0])+.05)]['test actual'].plot.hist()
    plt.figure();
    l = probdensityrv[(probdensityrv[0] > min(probdensityrv[0])-.05) & (probdensityrv[0] < min(probdensityrv[0])+.05)]['test actual'].plot.hist()

nnmodel()
nnmodelpredictpf(1, .85)
nnmodelpredictfl(1, .4)
nnmodelpredictefffl(1, .4)
nnmodelpredicttr(1, .4)
nnmodelpredictefftr(1, .4)
nnmodelpredictrv(1, .4)