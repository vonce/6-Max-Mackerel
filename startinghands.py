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
import bitarray as ba
import operator
import profile

deck1 = dk.Deck()
#print(deck.cardDeck)
startingHands = []
startingHands += itertools.combinations(deck1.deck, 2)

print('# of starting hands: ', len(startingHands))

cards = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']

#startingHandsTable = pd.DataFrame(np.zeros((13, 13),dtype = int),index = cards,columns = cards)

#for hand in startingHands:   
#    c1 = hand[0]
#    c2 = hand[1]
#    pos1 = np.absolute(c1[1]-14)
#    pos2 = np.absolute(c2[1]-14)
#    if c1[2] == c2[2]:
#        if pos1 > pos2:
#            startingHandsTable.iloc[pos2,pos1] = startingHandsTable.iloc[pos2,pos1] + 1
#        else:
#            startingHandsTable.iloc[pos1,pos2] = startingHandsTable.iloc[pos1,pos2] + 1
#    else:
#        if pos1 > pos2:
#            startingHandsTable.iloc[pos1,pos2] = startingHandsTable.iloc[pos1,pos2] + 1
#        else:
#            startingHandsTable.iloc[pos2,pos1] = startingHandsTable.iloc[pos2,pos1] + 1
#print(startingHandsTable)

def startinghandsequity(hands, board = ba.bitarray('0' * 52)):#LIST of hands
    deck = ba.bitarray('1' * 52)
    wins = np.zeros(len(hands))
    rankedhands = np.zeros(len(hands))
    s = 0
    
    for hand in hands:
        deck = ba.bitarray(map(operator.sub, deck, hand))
    for combo in itertools.combinations(deck.search(ba.bitarray('1')), 3):
        s = s + 1
        if s % 1000 == 0:
            print(s)
        n = ba.bitarray('0' * 52)
        for i in combo:
            n[i] = True
        for i in range(len(hands)):
            ba.bitarray(map(operator.add, hands[i], n))
            hr.handranker(ba.bitarray(map(operator.add, hands[i], n)))
        for i in range(len(hands)):
            pass

#    if board != []:
#        deck = ba.bitarray(map(operator.sub, deck, board))
#        boardlen = len(board)
#        
#        boards += itertools.combinations(d.deck, 5 - boardlen)
#        boards = [list(i) for i in boards]
#
#        for b in boards:
#            for i in range(len(hands)):
#                handranks[i] = hr.handranker(hands[i] + board + b)
#                
#            for i in range(len(handranks)):
#                #print(hr.showdown(handranks))
#                if handranks[i] in hr.showdown(handranks):
#                    wins[i] = wins[i] + 1
    #print(wins)
    print(wins)
#print(startinghandsequity([hr.cardstobit(['As','Js']),hr.cardstobit(['Ks','Kh'])]))
profile.run('startinghandsequity([hr.cardstobit([\'As\',\'Js\']),hr.cardstobit([\'Ks\',\'Kh\'])])')
