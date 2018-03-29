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
    
    def __init__(self, name, stack, hand, act = '', betamt = 0.0, board = [], pot = 0.0, bets = [], debt = 0.0, error = ''):
        self.name = name
        self.stack = stack
        self.hand = hand
        self.error = error
        self.debt = debt
        
    def action(self):
        print(self.error)
        print(self.name, self.hand)
        print(self.name, 'action: (check/fold) (bet/raise) (call) (allin)?')
        self.act = ''
        self.betamt = 0.0
        while (self.act != 'check/fold') & (self.act != 'bet/raise') & (self.act != 'call') & (self.act != 'allin'):
            self.act = input(':')
        if self.act == 'bet/raise':
            self.betamt = float(input('amount:'))
        if self.act == 'allin':
            self.betamt = self.stack
            self.stack = 0.0
        self.error = ''
        
    def reload(self):
        if self.stack < 200.0:
            self.debt = self.debt - (200 - self.stack)
            self.stack = 200.0
            

#print(x)
