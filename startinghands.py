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
import handrank as hr

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

def startinghandsequity(hands, board = []):#LIST of hands
    boardsfl = []
    handranks = [0] * len(hands)
    wins = [0] * len(hands)
    print(wins)
    d = dk.Deck()
    for h in hands:
        for j in range(len(h)):
            for i in d.deck:
                if i in h:
                    d.deck.remove(i)
#    print(d.deck)
    boardsfl += itertools.combinations(d.deck, 3)
    boardsfl = [list(i) for i in boardsfl]
#    boardstr += itertools.combinations(d.deck, 4)
#    boardsrv += itertools.combinations(d.deck, 5)
#    print(boardsfl)
    for b in boardsfl:
        for i in range(len(hands)):
            handranks[i] = hr.handranker(hands[i] + b)
            
        for i in range(len(handranks)):
            #print(hr.showdown(handranks))
            if handranks[i] in hr.showdown(handranks):
                wins[i] = wins[i] + 1
    #print(wins)
    wins = [i/len(boardsfl) for i in wins]
    print(wins)
        
startinghandsequity([[('As', 14, 0), ('Qs', 12, 0)],[('Ah', 14, 1),('Jh', 11, 1)],[('8h', 8, 2),('9h', 9, 2)]])
