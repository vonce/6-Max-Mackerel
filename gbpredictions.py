#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 14:21:22 2018

@author: Vince
"""
import pandas as pd
import numpy as np
import tools
from scipy.stats import gamma
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
df = pd.read_csv('data.csv')

def gbmodel():
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
    gbrhandstrengthpf = GradientBoostingRegressor()
    pipe = Pipeline([
            ('ss', sshandstrengthpf),
            ('gbr', gbrhandstrengthpf)
    ])
    params= {
    'max_depth': [1, 2, 3, 4, 5, 6, 7],
    'n_estimators': [100, 125, 150, 200, 300, 500],
    'max_features': ['auto', None]
    }
    modelpf = GridSearchCV(pipe, param_grid = params)
    modelpf.fit(X_train, y_train)
    print(modelpf.best_score_)
    print(modelpf.score(X_test, y_test))
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
    gbrhandstrengthfl = GradientBoostingRegressor()
    pipe = Pipeline([
            ('ss', sshandstrengthfl),
            ('gbr', gbrhandstrengthfl)
    ])
    modelfl = GridSearchCV(pipe, param_grid = params)
    modelfl.fit(X_train, y_train)
    print(modelfl.best_score_)
    print(modelfl.score(X_test, y_test))
    probdensityfl = pd.DataFrame(modelfl.predict(datafl.drop(['hand strength fl ^2','eff hand strength fl ^2'], axis = 1)))
    probdensityfl['test actual'] = list(datafl['hand strength fl ^2'])
    probdensityfl[0] = np.sqrt(probdensityfl[0])
    probdensityfl['test actual'] = np.sqrt(probdensityfl['test actual'])
    probdensityfl['diff'] = probdensityfl[0] - probdensityfl['test actual']

    X_train, X_test, y_train, y_test = train_test_split(datafl.drop(['hand strength fl ^2','eff hand strength fl ^2'], axis = 1),datafl['eff hand strength fl ^2'])
    sshandstrengthefffl = StandardScaler()
    gbrhandstrengthefffl = GradientBoostingRegressor()
    pipe = Pipeline([
            ('ss', sshandstrengthefffl),
            ('gbr', gbrhandstrengthefffl)
    ])
    modelefffl = GridSearchCV(pipe, param_grid = params)
    modelefffl.fit(X_train, y_train)
    print(modelefffl.best_score_)
    print(modelefffl.score(X_test, y_test))
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
    gbrhandstrengthtr = GradientBoostingRegressor()
    pipe = Pipeline([
            ('ss', sshandstrengthtr),
            ('gbr', gbrhandstrengthtr)
    ])
    modeltr = GridSearchCV(pipe, param_grid = params)
    modeltr.fit(X_train, y_train)
    print(modeltr.best_score_)
    print(modeltr.score(X_test, y_test))
    probdensitytr = pd.DataFrame(modeltr.predict(datatr.drop(['hand strength tr ^2','eff hand strength tr ^2'], axis = 1)))
    probdensitytr['test actual'] = list(datatr['hand strength tr ^2'])
    probdensitytr[0] = np.sqrt(probdensitytr[0])
    probdensitytr['test actual'] = np.sqrt(probdensitytr['test actual'])
    probdensitytr['diff'] = probdensitytr[0] - probdensitytr['test actual']

    X_train, X_test, y_train, y_test = train_test_split(datatr.drop(['hand strength tr ^2','eff hand strength tr ^2'], axis = 1),datatr['eff hand strength tr ^2'])
    sshandstrengthefftr = StandardScaler()
    gbrhandstrengthefftr = GradientBoostingRegressor()
    pipe = Pipeline([
            ('ss', sshandstrengthefftr),
            ('gbr', gbrhandstrengthefftr)
    ])
    modelefftr = GridSearchCV(pipe, param_grid = params)
    modelefftr.fit(X_train, y_train)
    print(modelefftr.best_score_)
    print(modelefftr.score(X_test, y_test))
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
    gbrhandstrengthrv = GradientBoostingRegressor()
    pipe = Pipeline([
            ('ss', sshandstrengthrv),
            ('gbr', gbrhandstrengthrv)
    ])
    modelrv = GridSearchCV(pipe, param_grid = params)
    modelrv.fit(X_train, y_train)
    print(modelrv.best_score_)
    print(modelrv.score(X_test, y_test))
    probdensityrv = pd.DataFrame(modelrv.predict(datarv.drop('hand strength rv ^2', axis = 1)))
    probdensityrv['test actual'] = list(datarv['hand strength rv ^2'])
    probdensityrv[0] = np.sqrt(probdensityrv[0])
    probdensityrv['test actual'] = np.sqrt(probdensityrv['test actual'])
    probdensityrv['diff'] = probdensityrv[0] - probdensityrv['test actual']
    #########rv
    print("river fitting complete")
    print("pf std", np.std(probdensitypf['diff']))
    print("fl std", np.std(probdensityfl['diff']))
    print("eff fl std", np.std(probdensityefffl['diff']))
    print("tr std", np.std(probdensitytr['diff']))
    print("eff tr std", np.std(probdensityefftr['diff']))
    print("rv std", np.std(probdensityrv['diff']))
    

def gbmodelpredictpf(pfinput):
    prediction = modelpf.predict(pfinput)
    print(prediction[0])
    distribution = probdensitypf[(probdensitypf[0] > prediction[0]-.025) & (probdensitypf[0] < prediction[0]+.025)]['test actual']
    fit_alpha, fit_loc, fit_beta=gamma.fit(distribution)
    pfhandranks = tools.pfhandranks()
    pfhandranks = pfhandranks.sort_values('rank')
    for i in pfhandranks.index:
        pfhandranks.at[i,'rank'] = gamma.pdf(pfhandranks.at[i,'rank'],fit_alpha, loc=fit_loc, scale=fit_beta)
    pfhandranks.plot.bar()
    return pfhandranks
    
def gbmodelpredictfl(flinput, flhandperc):
    prediction = modelfl.predict(flinput)
    distribution = probdensityfl[(probdensityfl[0] > prediction-.025) & (probdensityfl[0] < prediction+.025)]['test actual']
    fit_alpha, fit_loc, fit_beta=gamma.fit(distribution)
    #flhandperc = tools.handprobability()
    #flhandperc = flhandperc.sort_values('rank')
    for i in flhandperc.index:
        flhandperc.at[i,'rank'] = flhandperc.at[i,'rank']* gamma.pdf(flhandperc.at[i,'rank'],fit_alpha, loc=fit_loc, scale=fit_beta)
    return flhandperc

def gbmodelpredictefffl(flinput, effflhandperc):
    prediction = modelefffl.predict(flinput)
    distribution = probdensityefffl[(probdensityefffl[0] > prediction-.025) & (probdensityefffl[0] < prediction+.025)]['test actual']
    fit_alpha, fit_loc, fit_beta=gamma.fit(distribution)
    #flhandperc = tools.handprobability()
    #flhandperc = flhandperc.sort_values('rank')
    for i in effflhandperc.index:
        effflhandperc.at[i,'rank'] = effflhandperc.at[i,'rank']* gamma.pdf(effflhandperc.at[i,'rank'],fit_alpha, loc=fit_loc, scale=fit_beta)
    return effflhandperc

def gbmodelpredicttr(trinput, trhandperc):
    prediction = modeltr.predict(trinput)
    distribution = probdensitytr[(probdensitytr[0] > prediction-.025) & (probdensitytr[0] < prediction+.025)]['test actual']
    fit_alpha, fit_loc, fit_beta=gamma.fit(distribution)
    #flhandperc = tools.handprobability()
    #flhandperc = flhandperc.sort_values('rank')
    for i in trhandperc.index:
        trhandperc.at[i,'rank'] = trhandperc.at[i,'rank']* gamma.pdf(trhandperc.at[i,'rank'],fit_alpha, loc=fit_loc, scale=fit_beta)
    return trhandperc

def gbmodelpredictefftr(trinput, efftrhandperc):
    prediction = modelefftr.predict(trinput)
    distribution = probdensityefftr[(probdensityefftr[0] > prediction-.025) & (probdensityefftr[0] < prediction+.025)]['test actual']
    fit_alpha, fit_loc, fit_beta=gamma.fit(distribution)
    #flhandperc = tools.handprobability()
    #flhandperc = flhandperc.sort_values('rank')
    for i in efftrhandperc.index:
        efftrhandperc.at[i,'rank'] = efftrhandperc.at[i,'rank']* gamma.pdf(efftrhandperc.at[i,'rank'],fit_alpha, loc=fit_loc, scale=fit_beta)
    return efftrhandperc

def gbmodelpredictrv(rvinput, rvhandperc):
    prediction = modelefftr.predict(rvinput)
    distribution = probdensityrv[(probdensityrv[0] > prediction-.025) & (probdensityrv[0] < prediction+.025)]['test actual']
    fit_alpha, fit_loc, fit_beta=gamma.fit(distribution)
    #flhandperc = tools.handprobability()
    #flhandperc = flhandperc.sort_values('rank')
    for i in rvhandperc.index:
        rvhandperc.at[i,'rank'] = rvhandperc.at[i,'rank']* gamma.pdf(rvhandperc.at[i,'rank'],fit_alpha, loc=fit_loc, scale=fit_beta)
    return rvhandperc
#DELETE BELOW EVENTUALLY
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
datapfhand = data[['pf stack(bb)','#pl pf','position pf','position pf/#pl pf','pf bets(bb)','pf agg','stack/pfpot',
                   'tot bets pf/stack','log tot bets pf','log tot bets pf/stack','log tot agg pf',
                   'foldpf', 'callpf','raisepf', 'foldtoraisepf', 'reraisepf', 'foldtoreraisepf', 'pctseenfl',
                   'foldfl', 'callfl', 'betfl', 'raisefl', 'foldtoraisefl', 'reraisefl',
                   'pctseentr', 'foldtr', 'calltr', 'bettr', 'raisetr', 'foldtoraisetr',
                   'reraisetr', 'pctseenrv', 'foldrv', 'callrv', 'betrv', 'raiserv',
                   'foldtoraiserv', 'reraiserv', 'pctseensd']]
datapfhand = datapfhand.iloc[0].reshape(1,-1)

print(datapfhand)

   
#DELETE ABOVE EVENTUALLY
l = gbmodelpredictpf(datapfhand)
m = gbmodelpredictfl(1,l)
n = gbmodelpredictefffl(1,m)
o = gbmodelpredicttr(1,n)
p = gbmodelpredictefftr(1,o)
q = gbmodelpredictrv(1,p)