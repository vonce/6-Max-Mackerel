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
#    def checkfold(self):
    
#    def betraise(self, n):
        
#    def call(self):
#print(x)
