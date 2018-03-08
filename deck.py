# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 19:44:19 2018

@author: Vince
"""
from random import shuffle as shuff
import numpy as np

class Deck(object):#creates deck, iterates through all values and suits creates list of strings
    deck = []
    def __init__(self):
        self.deck = []
        for value in range(2,15):
            for suit_n in range (0,4):
                if suit_n == 0:
                    suit_s = 'c'
                if suit_n == 1:
                    suit_s = 'd'
                if suit_n == 2:
                    suit_s = 'h'
                if suit_n == 3:
                    suit_s = 's'
                cardstr = str(value) + suit_s
                if '10' in cardstr:
                    cardstr = cardstr.replace('10', 'T')
                if '11' in cardstr:
                    cardstr = cardstr.replace('11', 'J')
                if '12' in cardstr:
                    cardstr = cardstr.replace('12', 'Q')
                if '13' in cardstr:
                    cardstr = cardstr.replace('13', 'K')
                if '14' in cardstr:
                    cardstr = cardstr.replace('14', 'A')
                self.deck.append(cardstr)
                #self.deck.append(cardstr)
        self.deck = list(reversed(self.deck))
        self.numtocarddict = dict(zip(list(np.arange(0, 52)), list(self.deck)))
        self.cardtonumdict = dict(zip(list(self.deck), list(np.arange(0, 52))))
        
    def draw(self,to, num = 1):#draw from deck function, num is number of cards
        for _ in range(0, num):
            to.append(self.deck.pop(0))
    
    def shuffle(self):# shuffle function
        #self.__init__()
        shuff(self.deck)
        
d = Deck()
