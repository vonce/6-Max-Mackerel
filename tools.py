import pandas as pd
import numpy as np
import itertools
import deck as dk
import os
#os.environ['JAVA_HOME'] = "C:\Program Files\Java\jdk1.8.0_45"#type which java in terminal and paste here
os.environ['JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_161.jdk/Contents/Home"
os.environ['CLASSPATH'] = "./Flounder.jar"
from jnius import autoclass

calculate = autoclass("flounder.Calculate")

pfrank = pd.read_csv('./tables/linearrank.csv')
pfrank = pfrank.set_index(['Unnamed: 0'])
#print(pfequity.sort_values(by = ['1']))
pfallequity = pd.read_csv('./tables/allequity.csv')
pfallequity = pfallequity.set_index(['0'])

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

def startinghandsequity(h, h2):
    return pfallequity.at[simplehand(h2), simplehand(h)]

def startinghandsrank(h):
    return pfrank.at[simplehand(h), 'num']

def pfhandranks():
    startinghands = []
    d = dk.Deck()
    startinghands += itertools.combinations(d.deck, 2)
    startinghands = [str(h[0]) + str(h[1]) for h in startinghands]
    startinghands = pd.DataFrame(startinghands)
    startinghands['rank'] = [[h[0:2],h[2:4]] for h in startinghands[0]]
    startinghands['rank'] = [startinghandsrank(h) for h in startinghands['rank']]
    startinghands = startinghands.set_index(0)
    return startinghands

#def handpercsq(board):
#    startinghands = []
#    d = dk.Deck()
#    startinghands += itertools.combinations(d.deck, 2)
#    startinghands = [str(h[0]) + str(h[1]) for h in startinghands]
#    startinghands = pd.DataFrame(startinghands)
#    startinghands['rank'] = [[h[0:2],h[2:4]] for h in startinghands[0]]
#    startinghands['rank'] = [calculate.handequity(h,board) for h in startinghands['rank']]
#    startinghands = startinghands.set_index(0)
#    return startinghands

#handpercsq(['As','Kd','4s'])
#print(handpercsq)