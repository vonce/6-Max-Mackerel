#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:11:06 2018

@author: Vince
"""

import deck as dk
import itertools
import pandas as pd
import numpy as np

deck1 = dk.Deck()
#print(deck.cardDeck)
startingHands = []
startingHands += itertools.combinations(deck1.deck, 2)

print('# of starting hands: ', len(startingHands))

cards = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']

startingHandsTable = pd.DataFrame(np.zeros((13, 13),dtype = int),index = cards,columns = cards)

for hand in startingHands:   
    c1 = hand[0]
    c2 = hand[1]
    pos1 = np.absolute(c1[1]-14)
    pos2 = np.absolute(c2[1]-14)
    if c1[2] == c2[2]:
        if pos1 > pos2:
            startingHandsTable.iloc[pos2,pos1] = startingHandsTable.iloc[pos2,pos1] + 1
        else:
            startingHandsTable.iloc[pos1,pos2] = startingHandsTable.iloc[pos1,pos2] + 1
    else:
        if pos1 > pos2:
            startingHandsTable.iloc[pos1,pos2] = startingHandsTable.iloc[pos1,pos2] + 1
        else:
            startingHandsTable.iloc[pos2,pos1] = startingHandsTable.iloc[pos2,pos1] + 1
print(startingHandsTable)

