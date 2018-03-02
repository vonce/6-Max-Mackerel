# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 19:44:19 2018

@author: Vince
"""
from random import shuffle as shuff

class Deck(object):
    deck = []
    def __init__(self):
        self.deck = []
        for suit_n in range(0,4):
            for value in range (2,15):
                if suit_n == 0:
                    suit_s = 's'
                if suit_n == 1:
                    suit_s = 'h'
                if suit_n == 2:
                    suit_s = 'd'
                if suit_n == 3:
                    suit_s = 'c'
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
                self.deck.append((cardstr, value, suit_n))
        self.deck = list(self.deck)
        
    def draw(self,to, num = 1):
        for _ in range(0, num):
            to.append(self.deck.pop(0))
    
    def shuffle(self):
        #self.__init__()
        shuff(self.deck)
        
