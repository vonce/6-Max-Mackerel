#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:50:33 2018

@author: Vince
"""

class Player(object):
    name = ''
    hand = []
    stack = 0.0
    
    def __init__(self, name, stack, hand):
        self.name = name
        self.stack = stack
        self.hand = hand
    def action(self, origbetbehind = 0.0):
        print(self.name, 'action: ', 'check/fold', 'bet/raise', 'call?')
        act = ''
        betamt = 0.0
        while (act != 'check/fold') & (act != 'bet/raise') & (act != 'call'):
            act = input(':')
        if act == ('bet/raise'):
            while (betamt > self.stack) | (betamt < 2.0) | ((origbetbehind != 0.0) & (betamt < origbetbehind * 2)):
                betamt = float(input('amount:'))
                if betamt > self.stack:
                    print('stack too small')
                if betamt < 2.0:
                    print('min bet is at least a big blind')
                if (origbetbehind != 0.0) & (betamt < origbetbehind * 2):
                    print('raise must be at least double original bet')




#print(x)
