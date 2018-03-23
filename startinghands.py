#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:11:06 2018

@author: Vince
"""
import os
os.environ['JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_161.jdk/Contents/Home"#type which java in terminal and paste here
os.environ['CLASSPATH'] = "./Flounder.jar"
from jnius import autoclass
import deck as dk
import itertools
import pandas as pd
import numpy as np
import timeit
calculate = autoclass("flounder.Calculate")

twosuitdeck = dk.Deck()
for i in range(26):
    del twosuitdeck.deck[-1]

print(twosuitdeck.deck)

twosuithands = []
df = []
time = 0.0
twosuithands += itertools.combinations(twosuitdeck.deck, 2)

for hand in twosuithands:
    start = timeit.default_timer()
    totequity = 0.0
    deck1 = dk.Deck()
    for i in hand:
        deck1.deck.remove(i)
    startingHands = []
    startingHands += itertools.combinations(deck1.deck, 2)
    print('# of starting hands: ', len(startingHands))

    for hs in startingHands:
        equity = calculate.equity([], [hand, hs])[0][0]
        print(hand, hs, equity)
        totequity = totequity + equity
    totequity = totequity/len(startingHands)
    stop = timeit.default_timer()
    time = round(time + stop - start, 2)
    print('Total elapsed:', time, 'sec.\n')
    df.append((hand, totequity))
    print(df)

df= pd.DataFrame(df)

cards = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']

startingHandsTable = pd.DataFrame(np.zeros((13, 13),dtype = int),index = cards,columns = cards)

print(df)

df.to_csv('startinghands.csv')