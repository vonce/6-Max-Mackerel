import pandas as pd
import numpy as np

pfequity = pd.read_csv('./tables/totalequity.csv')
#print(pfequity.columns)
pfequity = pfequity.drop('Unnamed: 0', axis = 1)
##print(pfequity.sort_values(by = ['1']))
#print(pfequity['1'].min())
pfequity['1'] = pfequity['1'] - pfequity['1'].min()
pfequity['1'] = pfequity['1']/pfequity['1'].max()
pfequity = pfequity.set_index(['0'])
#print(pfequity.sort_values(by = ['1']))

def startinghandsrank(h):
    return pfequity.at[simplehand(h), '1']

def simplehand(hand):
    simphand = ""
    for i in hand:
        simphand = simphand + i[0]
    if (simphand[0] < simphand[1]):
        simphand = simphand[::-1]
    if (simphand[1] == 'A'):
        simphand = simphand[::-1]
    if (simphand[1] == 'K') & (simphand[0] != 'A'):
        simphand = simphand[::-1]
    if (simphand[1] == 'Q') & ((simphand[0] != 'A') & (simphand[0] != 'K')):
        simphand = simphand[::-1]
    if (simphand[1] == 'J') & ((simphand[0] != 'A') & (simphand[0] != 'K') & (simphand[0] != 'Q')):
        simphand = simphand[::-1]
    if hand[0][0] != hand[1][0]:
        if hand[0][1] != hand[1][1]:
            simphand = simphand + "o"
        else:
            simphand = simphand + "s"
    return simphand
