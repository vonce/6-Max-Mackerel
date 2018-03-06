#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 15:50:33 2018

@author: Vince
"""
import itertools
import timeit
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
def long(n):
    j = []
    for i in itertools.permutations(np.arange(0,n),4):
        j.append(i)
    return j


start = timeit.default_timer()

print(len(long(60)))

stop = timeit.default_timer()

print(stop - start)