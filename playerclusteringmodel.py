import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans, k_means
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, FunctionTransformer, Imputer
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

stats = pd.read_csv('stats.csv')
print(stats)
print(stats.columns)
print(stats.shape)

modelstats = stats[stats['numplayedpf'] > 500]
#unnamedlist = []
#for c in list(stats.columns):
#    if 'Unnamed' in c:
#        unnamedlist.append(c)
#    print(unnamedlist)
#stats = stats.drop(unnamedlist, axis = 1)

print(modelstats.shape)

modeldropcol = ['Unnamed: 0', 'avgstack', 'net', 
                'numraisedpf', 'numreraisedpf', 'numplayedpf',
                'numraisedfl', 'numreraisedfl', 'numplayedfl', 'foldtoreraisefl',
                'numraisedtr', 'numreraisedtr', 'numplayedtr', 'foldtoreraisetr',
                'numraisedrv', 'numreraisedrv', 'numplayedrv', 'foldtoreraiserv',
                'numplayedsd',
                'bb/100hands', 'winpercent'
                ]

X = modelstats.drop(modeldropcol, axis = 1)
predictablestats = stats.drop(modeldropcol, axis = 1)
#modelcol = ['foldpf', 'foldtoraisepf', 'callpf', 'raisepf','pctseenfl', 'pctseentr', 'pctseenrv', 'pctseensd',]

#X = modelstats[modelcol]
#predictablestats = stats[modelcol]
print(X.columns)
ss = StandardScaler()

ss.fit(X)

X = ss.transform(X)
km = KMeans(n_clusters = 4).fit(X)

#dbscan        =  DBSCAN(eps=2.5, min_samples=10).fit(X)
#core_samples  =  dbscan.core_sample_indices_
#print(core_samples)
labels        =  km.labels_
#print(set(labels))
#labels = list(labels)

modelstats['cluster'] = labels
#for i in list(set(labels)):
#    print(i, ':', labels.count(i))
predictablestats = ss.transform(predictablestats)

print(km.predict(predictablestats))
stats['cluster'] = km.predict(predictablestats)


print(modelstats.groupby('cluster').count())
print(modelstats.groupby('cluster').mean())
print(modelstats.corr()['bb/100hands'].sort_values())

ax2 = sns.heatmap(modelstats.corr())
fig, ax = plt.subplots()

colors = {0:'red', 1:'blue', 2:'green', 3:'black', 4:'yellow', 5:'orange', 6:'purple', 7:'cyan', 8:'magenta', 9:'brown'}

ax.scatter(modelstats['callpf'], modelstats['bb/100hands'], c=modelstats['cluster'].apply(lambda x: colors[x]))

plt.show()
#print(stats[stats['cluster'] == 0])

stats.to_csv('clusteredstats.csv')