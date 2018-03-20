# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 20:16:39 2018

@author: Vince
"""
#OUTDATED
#I have written most of these in java now and it is much faster
import itertools
import deck as dk
import pandas as pd
import numpy as np
import bitarray as ba
import operator
import timeit

def cardstobit(cards):# turns list of cards(strings) to 52 bit array
    bitarr = ba.bitarray('0' * 52)
    for n in [dk.d.cardtonumdict[card] for card in cards]:
        bitarr[n] = True
    return bitarr

def bittocards(bitarr):# turns 52 bit array to list of cards(strings)
    cards = bitarr.search(ba.bitarray('1'))
    cards = [dk.d.numtocarddict[num] for num in cards]
    return cards

def straightflush(bitarr):# Assess hand for straight flush, returns 5 card hand in bit array
    cardlist = (bitarr.search(ba.bitarray('1')))
    h = ba.bitarray('0' * 52)
    for i in cardlist:
        if (bitarr[i:i+17:4] == ba.bitarray('11111')):
            h[i:i+17:4] = bitarr[i:i+17:4]
            return (h, int((i - i % 4) / 4))
        elif ((36<=i) & (i<40)) & (bitarr[i:i+17:4] == ba.bitarray('1111')) & (bitarr[i % 4] == True):#Special 'wheel' case
            h[i:i+17:4] = bitarr[i:i+17:4]
            h[i%4] = bitarr[i%4]
            return (h, (int((i - i % 4) / 4),))
    return False

def quads(bitarr):# Assess hand for quads, returns 5 card hand in bit array
    cardlist = (bitarr.search(ba.bitarray('1')))
    h = ba.bitarray('0' * 52)
    for i in cardlist:
        if (i % 4 == 0) & (bitarr[i:i+4] == ba.bitarray('1111')):
            h[i:i+4] = bitarr[i:i+4]
            for j in cardlist:
                if h[j] == False:
                    h[j] = bitarr[j]
                    break
            return (h, (int((i - i % 4) / 4), int((j - j % 4) / 4)))
    return False

def fullhouse(bitarr):# Assess hand for fullhouse, returns 5 card hand in bit array
    cardlist = (bitarr.search(ba.bitarray('1')))
    h = ba.bitarray('0' * 52)
    for i in cardlist:
        j = i - i % 4
        if bitarr[j:j+4].count() >= 3:
            for l in range(4):
                if (bitarr[j:j+4-l].count() == 3):
                    h[j:j+4-l] = bitarr[j:j+4-l]
            break
    for i in cardlist:
        k = i - i % 4
        if (bitarr[k:k+4].count() >= 2) & (k != j) & (h.count() == 3):
            for l in range(4):
                if (bitarr[k:k+4-l].count() == 2):
                    h[k:k+4-l] = bitarr[k:k+4-l]
                    return (h, (int(j / 4), int(k / 4)))
    return False

def flush(bitarr):# Assess hand for flush, returns 5 card hand in bit array
    cardlist = (bitarr.search(ba.bitarray('1')))
    h = ba.bitarray('0' * 52)
    for i in cardlist:
        if bitarr[i:i+52:4].count() >= 5:
            for j in range(13):
                if h[i:i+52:4].count() < 5:
                    h[i+(j*4)] = bitarr[i+(j*4)]
                else:
                    break
            return (h, tuple([int((_ - _ % 4) / 4) for _ in h.search(ba.bitarray('1'))]))
    return False    
            
def straight(bitarr):# Assess hand for straight, returns 5 card hand in bit array
    cardlist = (bitarr.search(ba.bitarray('1')))
    h = ba.bitarray('0' * 52)
    for i in cardlist:
        l = 0
        j = i - i % 4
        for k in range(5):
            if bitarr[j+k*4:j+k*4+4].count() >= 1:
                l = l + 1
            if l == 5:
                for m in range(5):
                    for n in range(4):
                        if (bitarr[j+m*4:j+m*4+4-n].count() == 1):
                            h[j+m*4:j+m*4+4-n] = bitarr[j+m*4:j+m*4+4-n]
                            break
                return (h, (int((i - i % 4) / 4),))
        if ((36<=i) & (i<40)) & (bitarr[0:4].count() >= 1):
            l = 0
            for k in range(4):
                if bitarr[j+k*4:j+k*4+4].count() >= 1:
                    l = l + 1
                if l == 4:
                    
                    for m in range(5):
                        for n in range(4):
                            if (bitarr[j+m*4:j+m*4+4-n].count() == 1):
                                h[j+m*4:j+m*4+4-n] = bitarr[j+m*4:j+m*4+4-n]
                                break
                        for n in range(4):
                            if (bitarr[0:4-n].count() == 1):
                                h[0:4-n] = bitarr[0:4-n]
                                break
                    return (h, (int((i - i % 4) / 4),))
    return False

def trips(bitarr):# Assess hand for three of a kind, returns 5 card hand in bit array
    cardlist = (bitarr.search(ba.bitarray('1')))
    h = ba.bitarray('0' * 52)
    for i in cardlist:
        if (bitarr[i:i+4].count() >= 3):
            for j in range(4):
                if bitarr[i:i+4-j].count() == 3:
                    h[i:i+4-j] = bitarr[i:i+4-j]
                    break
            for j in cardlist:
                if (h[j] == False) & (h.count() != 5):
                    h[j] = True
                    if h.count() == 4:
                        k = j
                    if h.count() == 5:
                        return (h, (int((i - i % 4) / 4), int((k - k % 4) / 4), int((j - j % 4) / 4)))
                    
    return False 

def twopair(bitarr):# Assess hand for two pair, returns 5 card hand in bit array
    cardlist = (bitarr.search(ba.bitarray('1')))
    h = ba.bitarray('0' * 52)
    for i in cardlist:
        j = i - i % 4
        if bitarr[j:j+4].count() >= 2:
            for l in range(4):
                if (bitarr[j:j+4-l].count() == 2):
                    h[j:j+4-l] = bitarr[j:j+4-l]
            break
    for m in cardlist:
        k = m - m % 4
        if (bitarr[k:k+4].count() >= 2) & (k != j) & (h.count() == 2):
            for l in range(4):
                if (bitarr[k:k+4-l].count() == 2):
                    h[k:k+4-l] = bitarr[k:k+4-l]
                    for j in cardlist:
                        if (h[j] == False) & (h.count() != 5):
                            h[j] = True 
                            return (h, (int((i - i % 4) / 4), int((m - m % 4) / 4), int((j - j % 4) / 4)))
    return False

def pair(bitarr):# Assess hand for pair, returns 5 card hand in bit array
    cardlist = (bitarr.search(ba.bitarray('1')))
    h = ba.bitarray('0' * 52)
    for i in cardlist:
        j = i - i % 4
        if bitarr[j:j+4].count() >= 2:
            for l in range(4):
                if (bitarr[j:j+4-l].count() == 2):
                    h[j:j+4-l] = bitarr[j:j+4-l]
                    break
            for j in cardlist:
                if (h[j] == False) & (h.count() != 5):
                    h[j] = True
                    if h.count() == 3:
                        k = j
                    if h.count() == 4:
                        l = j
                    if h.count() == 5:
                        return (h, (int((i - i % 4) / 4), int((k - k % 4) / 4), int((l - l % 4) / 4), int((j - j % 4) / 4)))             
    return False

def nothing(bitarr):# Assess hand for best 5 card high hand, returns 5 card hand in bit array
    cardlist = (bitarr.search(ba.bitarray('1')))
    h = ba.bitarray('0' * 52)
    for i in cardlist:
        if (h[i] == False) & (h.count() != 5):
            h[i] = True
            if h.count() == 5:
                break
    return (h, tuple([int((_ - _ % 4) / 4) for _ in h.search(ba.bitarray('1'))]))

def handranker(bitarr):# takes card bit array to find best 5 card hand, ranks between 0-8
    if straightflush(bitarr):
        return (straightflush(bitarr), 0)
    if quads(bitarr):
        return (quads(bitarr), 1)
    if fullhouse(bitarr):
        return (fullhouse(bitarr), 2)
    if flush(bitarr):
        return (flush(bitarr), 3)
    if straight(bitarr):
        return (straight(bitarr), 4)
    if trips(bitarr):
        return (trips(bitarr), 5)
    if twopair(bitarr):
        return (twopair(bitarr), 6)
    if pair(bitarr):
        return (pair(bitarr), 7)
    return (nothing(bitarr), 8)

def showdown(hands):# takes hands with rank generated by handranker to find winners
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

def handpercentile(hand = ba.bitarray('0' * 52), board = ba.bitarray('0' * 52)):#takes a 2 card hand and a board and ranks it compared to all other 2 card hands against the board, ranking from 0-1
    ranklist = []
    ranknum = []
    deck = ba.bitarray('1' * 52)
    deck = ba.bitarray(map(operator.sub, deck, hand))
    deck = ba.bitarray(map(operator.sub, deck, board))
    start = timeit.default_timer()
    for combo in itertools.combinations(deck.search(ba.bitarray('1')), 2):   
        n = ba.bitarray('0' * 52)
        for i in combo:
            n[i] = True
        h = n
        n = ba.bitarray(map(operator.add, n, board))
        ranklist.append((handranker(n),h))
    ranklist.append((handranker(ba.bitarray(map(operator.add, hand, board))), hand))
    ranklist = sorted(ranklist, key=lambda x: (x[0][1], x[0][0][1]))
    for i in range(len(ranklist)):
        if (ranklist[i][0][0][1] == ranklist[i-1][0][0][1]) & (ranknum != []):
            ranknum.append(ranknum[i-1])
        else:
            ranknum.append(i)
    ranknum = [1 - (i/len(ranknum)) for i in ranknum]
    stop = timeit.default_timer()
    print('sort and data:',stop - start)
    return ranknum[ranklist.index((handranker(ba.bitarray(map(operator.add, hand, board))), hand))]

#x = handpercentile(cardstobit(['Jd','4s']),cardstobit(['Td','Qd','Ad','9s','7s']))
#y = bittocards(handranker(cardstobit(['2s','Qh','Td','2c','As','9d','7s']))[0][0])
#print(x)
  
def draws(handd, boardd):# counts draws, may be replaced?
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
        
def boardtexture(boardtext):# SLOW. created technique to find board texture static - dynamic
    avgrankdiff = []
    df = []
    df2 = []
    a = 0
    if boardtext:
        deck = ba.bitarray('1' * 52)
        deck = ba.bitarray(map(operator.sub, deck, boardtext))
        for combo in itertools.combinations(deck.search(ba.bitarray('1')), 2):
            print(a)
            a = a + 1
            n = ba.bitarray('0' * 52)
            for i in combo:
                n[i] = True
            h = n
            n = ba.bitarray(map(operator.add, n, boardtext))
            df.append((handpercentile(n), h))
            deck = ba.bitarray(map(operator.sub, deck, n))
            for card in itertools.combinations(deck.search(ba.bitarray('1')), 1):
                m = ba.bitarray('0' * 52)
                m[i] = True
                m = ba.bitarray(map(operator.add, m, boardtext))
                m = ba.bitarray(map(operator.add, m, n))
                df2.append((handpercentile(m), h))
        df[0] = [tuple(i[1]) for i in df[0]]
        df.columns = ['cards', 'rank']
        df2[0] = [tuple(i[1]) for i in df2[0]]
        df2.columns = ['cards', 'rank2']
        df = df.merge(df2, on = 'cards')
        df['rankdiff'] = (df['rank'] - df['rank2']) ** 2
        avgrankdiff.append(np.mean(df['rankdiff']))
        staticdynamic = np.mean(avgrankdiff)
    return staticdynamic

#print(boardtexture(cardstobit(['Ah','Qs','8h'])))

def convert(cards):# 'card string' --> ('card string', int, int) card notation
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

#hnd = [('Ac', 14, 3), ('Ah', 14, 1)]
#brd = [('Qc', 12, 3), ('4d', 4, 2), ('6h', 6, 1), ('Tc', 10, 3), ('As', 14, 0)]
#print('hole cards:', hnd)
#print('board:', brd)
#print(handrankboard(hnd, brd) ** 2)
#print(draws(hnd, brd))
