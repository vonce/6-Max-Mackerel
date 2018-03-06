# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 20:16:39 2018

@author: Vince
"""

import itertools
import deck as dk
import pandas as pd
import numpy as np

def quads(hand):
    _ = []
    for card in hand:
        _.append(card[1])
    _.sort(reverse = True)
    j = 0
    k = 0
    for i in _:
        if i == _[j-1]:
            k = k+1
            if k == 3:
                while i in _:
                    _.remove(i)
                return i
        else:
            k = 0
        j = j+1
    return False

def fullhouse(hand):
    _ = []
    for card in hand:
        _.append(card[1])
    _.sort(reverse = True)
    j = 0
    k = 0
    for i in _:
        if i == _[j-1]:
            k = k+1
            if k == 2:
                while i in _:
                    _.remove(i)
                    house = i
                k = 0
                j = 0
                for l in _:
                    if l == _[j-1]:
                        fullof = l
                        return house, fullof
                    j = j+1
                return False
        else:
            k = 0
        j = j+1
    return False        

def pair(hand):
    _ = []
    for card in hand:
        _.append(card[1])
    _.sort(reverse = True)
    j = 0
    for i in _:
        if i == _[j-1]:
            return i
        j = j+1
    return False

def twopair(hand):
    _ = []
    for card in hand:
        _.append(card[1])
    _.sort(reverse = True)
    j = 0
    for i in _:
        if i == _[j-1]:
            while i in _:
                _.remove(i)
                pair1 = i
            j = 0
            for l in _:
                if l == _[j-1]:
                    pair2 = l
                    return pair1, pair2
                j = j+1
            return False
        j = j+1
    return False

def threekind(hand):
    _ = []
    for card in hand:
        _.append(card[1])
    _.sort()
    j = 0
    k = 0
    for i in _:
        if i == _[j-1]:
            k = k+1
            if k == 2:
                return i
        else:
            k = 0
        j = j+1
    return False        

def flush(hand):
    _ = []
    for card in hand:
        _.append(card[2])
    __ = set(_)
    for i in __:
        j = 0
        if j < _.count(i):
            j = _.count(i)
            if j > 4:
                return True
    return False
            
def straight(hand):
    _ = []
    for card in hand:
        _.append(card[1])
    __ = list(set(_))
    __.sort(reverse = True)
    j= 0
    k = 0
    for i in __:
        if (i+1 == __[j-1]):
            k = k+1
            if ((__[0] == 14) & (i == 2)) == True: # The Wheel
                k = k+1
            if k == 4:
                if (__[0] != 14) | (i != 2):
                    return i+4
                else:
                    return 5
        else:
            k = 0
        j = j+1
    return False
    
def straightflush(hand):
    if (straight(hand) != False) & (flush(hand) != False):
        return straight(hand)
    else:
        return False
    

def handranker(hand):
    rank = 0
    bestrank = 0
    h = ([(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],0)
    for hand5 in itertools.combinations(hand,5):
        hand5 = sorted(hand5, key=lambda x: x[1], reverse= True)
        
        if straightflush(hand5) != False:
            if straight(hand5) == 5:
                hand5 += [hand5.pop(0)]
            rank = 8
        elif quads(hand5) != False:
            i = 0
            for card in hand5:  
                if card[1] == quads(hand5):
                    hand5.insert(0, hand5.pop(i))                    
                i = i + 1
            rank = 7
        elif fullhouse(hand5) != False:
            i = 0
            for card in hand5:  
                if card[1] == fullhouse(hand5)[1]:
                    hand5.insert(0, hand5.pop(i))                    
                i = i + 1
            i = 0
            for card in hand5:  
                if card[1] == fullhouse(hand5)[0]:
                    hand5.insert(0, hand5.pop(i))                    
                i = i + 1
            rank = 6
        elif flush(hand5) != False:
            rank = 5
        elif straight(hand5) != False:
            if straight(hand5) == 5:
                hand5 += [hand5.pop(0)]
            rank = 4
        elif threekind(hand5) != False:
            i = 0
            for card in hand5:  
                if card[1] == threekind(hand5):
                    hand5.insert(0, hand5.pop(i))                    
                i = i + 1
            rank = 3
        elif twopair(hand5) != False:
            i = 0
            for card in hand5:  
                if card[1] == twopair(hand5)[1]:
                    hand5.insert(0, hand5.pop(i))                    
                i = i + 1
            i = 0
            for card in hand5:  
                if card[1] == twopair(hand5)[0]:
                    hand5.insert(0, hand5.pop(i))                    
                i = i + 1
            rank = 2
        elif pair(hand5) != False:
            i = 0
            for card in hand5:  
                if card[1] == pair(hand5):
                    hand5.insert(0, hand5.pop(i))
                i = i + 1
            rank = 1
        else:
            rank = 0

        if rank > bestrank:
            bestrank = rank
            h = (hand5, rank)
            
        elif rank == bestrank:
            i = 0
            for card in hand5:         
                if card[1] > h[0][i][1]:
                    h = (hand5, rank)
                    break
                elif card[1] == h[0][i][1]:
                    i = i + 1
                else:
                    break
    return h

def showdown(hands):
    winners = []
    h = ([(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],0)
    ranks = [[],[],[],[],[],[],[],[],[],[]]
    ordered = []
    for hand in hands:
        if hand[1] == 0:
            ranks[0].append(hand)
        if hand[1] == 1:
            ranks[1].append(hand)
        if hand[1] == 2:
            ranks[2].append(hand)
        if hand[1] == 3:
            ranks[3].append(hand)
        if hand[1] == 4:
            ranks[4].append(hand)
        if hand[1] == 5:
            ranks[5].append(hand)
        if hand[1] == 6:
            ranks[6].append(hand)
        if hand[1] == 7:
            ranks[7].append(hand)
        if hand[1] == 8:
            ranks[8].append(hand)
    for i in range(len(ranks)):
        ranks[i] = sorted(ranks[i], key = lambda x: (x[0][0][1], x[0][1][1], x[0][2][1], x[0][3][1], x[0][4][1]))
    
    for i in range(len(ranks)):
        ordered = ordered + ranks[i]
    
    numberrank = []
    ordered = list(reversed(ordered))

    for i in ordered:
        _ = 0
        for j in range(len(i[0])):
            if (i[0][j][1] != h[0][j][1])|(i[1] != h[1]):
                numberrank.append(ordered.index(i))
                break
            else:
                _ = _ + 1
                if _ == 5:
                    _ = 0
                    numberrank.append(ordered.index(i) - 1)
                    break
        h = i
    for i in range(len(numberrank)):
        if max(numberrank) == 0:
            num = 1
        else:
            num = max(numberrank)
        numberrank[i] = abs(numberrank[i] - num)
    numberrank = [j/num for j in numberrank]

    for i in range(len(ordered)):   
        if numberrank[i] == 1:
            winners.append(ordered[i])
    
    #print(numberrank)
    #print(ordered)
    return winners

def handrankboard(hand = [], board = []):
    hnd = (([(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)],0),[(0,0,0),(0,0,0)])
    #TUPLE(TUPLE(best 5 card hand, rank),hole cards)
    ranks = [[],[],[],[],[],[],[],[],[],[]]
    ordered = []
    
    if board:
        d = dk.Deck()
        for j in range(len(hand)):
            for i in d.deck:
                if i in hand:
                    d.deck.remove(i)
        for j in range(len(board)):
            for i in d.deck:
                if i in board:
                    d.deck.remove(i)
                    
        startingHands = []
        startingHands += itertools.combinations(d.deck, 2)
        for i in range(len(startingHands)):
            startingHands[i] = sorted(startingHands[i], key = lambda x: x[1], reverse = True)
        if hand:
            startingHands.append(hand)
        hands = []
        for i in range(len(startingHands)):
            startingHands[i] = list(startingHands[i])
            j = (handranker(startingHands[i] + board), startingHands[i])
            hands.append(j)
        
        for h in hands:
            if h[0][1] == 0:
                ranks[0].append((h[0],h[1]))
            if h[0][1] == 1:
                ranks[1].append((h[0],h[1]))
            if h[0][1] == 2:
                ranks[2].append((h[0],h[1]))
            if h[0][1] == 3:
                ranks[3].append((h[0],h[1]))
            if h[0][1] == 4:
                ranks[4].append((h[0],h[1]))
            if h[0][1] == 5:
                ranks[5].append((h[0],h[1]))
            if h[0][1] == 6:
                ranks[6].append((h[0],h[1]))
            if h[0][1] == 7:
                ranks[7].append((h[0],h[1]))
            if h[0][1] == 8:
                ranks[8].append((h[0],h[1]))
            if h[1] == hand:
                hand = h
        for i in range(len(ranks)):
            ranks[i] = sorted(ranks[i], key = lambda x: (x[0][0][0][1], x[0][0][1][1], x[0][0][2][1], x[0][0][3][1], x[0][0][4][1]))
        for i in range(len(ranks)):
            ordered = ordered + ranks[i]
        ordered = list(reversed(ordered))

        numberrank = []
        for i in ordered:
            _ = 0
            
            for j in range(len(i[0][0])):
                if i[0][0][j][1] != hnd[0][0][j][1]:
                    numberrank.append(ordered.index(i))
                    break
                else:
                    _ = _ + 1
                    if _ == 5:
                        _ = 0
                        numberrank.append(numberrank[ordered.index(i) - 1])
                        break
            hnd = i

        for i in range(len(numberrank)):
            numberrank[i] = abs(numberrank[i] - len(numberrank))
#        print(ordered)
#        print(numberrank)
        ordered = pd.Series(ordered)
        numberrank = pd.Series(numberrank)
        numberrank = numberrank/max(numberrank)

#        numberrank = numberrank ** 3

        dfranks = pd.concat([ordered, numberrank], axis = 1)

        if hand:
            return (dfranks.loc[dfranks[0] == hand].get_values()[0][1])
        else:
            return dfranks
    else:
        return 0# CODE FOR NO BOARD HOLECARDS GOES HERE
  
def draws(handd, boardd):
    b = boardd
    if boardd:
        d = dk.Deck()
        for j in range(len(handd)):
            for i in d.deck:
                if i in handd:
                    d.deck.remove(i)
        for j in range(len(boardd)):
            for i in d.deck:
                if i in boardd:
                    d.deck.remove(i)
    flushdraws = 0
    straightdraws = 0
    straightflushdraws = 0
    for cardd in d.deck:
        if handranker(b + handd)[1] <= 1:
            c = [cardd]        
            rank = handranker(b + handd + c)
            if (rank[1] == 8) & ((handd[0] in rank[0])|(handd[1] in rank[0])):
                straightflushdraws = straightflushdraws + 1
            if rank[1] == 5:
                flushdraws = flushdraws + 1
            if rank[1] == 4:
                straightdraws = straightdraws + 1
            
    return (flushdraws, straightdraws, straightflushdraws)
        
def boardtexture(boardtext):
    avgrankdiff = []
    if boardtext:
        d = dk.Deck()
        for j in range(len(boardtext)):
            for i in d.deck:
                if i in boardtext:
                    d.deck.remove(i)
        for card in d.deck:
            df = handrankboard(board = boardtext)
            df2 = handrankboard(board = boardtext + [card])
            df[0] = [tuple(i[1]) for i in df[0]]
            df.columns = ['cards', 'rank']
            df2[0] = [tuple(i[1]) for i in df2[0]]
            df2.columns = ['cards', 'rank2']
            df = df.merge(df2, on = 'cards')
            df['rankdiff'] = (df['rank'] - df['rank2']) ** 2
            avgrankdiff.append(np.mean(df['rankdiff']))
        staticdynamic = np.mean(avgrankdiff)
    return staticdynamic
    
                  
def convert(cards):# 'string' --> ('string', int, int)
    convcards = []
    if cards:
        for card in cards:
            val = card[0]
            suit = card[1]
            if val == 'T':
                val = 10
            if val == 'J':
                val = 11
            if val == 'Q':
                val = 12
            if val == 'K':
                val = 13
            if val == 'A':
                val = 14
            if suit == 's':
                suit = 0
            if suit == 'h':
                suit = 1
            if suit == 'd':
                suit = 2
            if suit == 'c':
                suit = 3
            convcards.append((card, int(val), int(suit)))
        return convcards

        
print(boardtexture([('Ks', 13, 0), ('3c', 3, 3), ('8h', 8, 1)]))

#deck1 = dk.Deck()          
#ranklist = []
#numdraw = 3
#iterations = 1000

#showdownlist = []
#for i in range(0,iterations):
#    d = []
#    h = []
#    deck1.__init__()
#    h.append(deck1.deck.pop(51))
#    h.append(deck1.deck.pop(50))
#    deck1.shuffle()
#    deck1.draw(d,numdraw)
#    showdownlist.append(handranker(d+h))
#    ranklist.append(handranker(d+h)[1])
#print(h)
#print('drawing', numdraw, 'cards with', iterations,'samples')

#handdict = {
#        0: 'nothing',
#        1: 'pair',
#        2: 'two pair',
#        3: 'three of a kind',
#        4: 'straight',
#        5: 'flush',
#        6: 'full house',
#        7: 'quads',
#        8: 'straight flush'
#        }

#ranklist = pd.Series(ranklist)
#tot = len(ranklist)
#ranklist = ranklist.value_counts()
#ranklist = pd.DataFrame(ranklist/tot)
#ranklist.rename(index = handdict, inplace = True)

#print(ranklist)

hnd = [('Ac', 14, 3), ('Ah', 14, 1)]
brd = [('Qc', 12, 3), ('4d', 4, 2), ('6h', 6, 1), ('Tc', 10, 3), ('As', 14, 0)]
print('hole cards:', hnd)
print('board:', brd)
print(handrankboard(hnd, brd) ** 2)
print(draws(hnd, brd))
