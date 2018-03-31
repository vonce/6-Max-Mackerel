#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:01:19 2018

@author: Vince
"""
import os
os.environ['JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_161.jdk/Contents/Home"#type which java in terminal and paste here
os.environ['CLASSPATH'] = "./Flounder.jar"
from jnius import autoclass
import player as pl
import mackerel as mk
import deck as dk

calculate = autoclass("flounder.Calculate")

class Table(object):
    players = []
    bigblind = 0.0
    bets = []
    pot = 0.0
    d = []
    board = []
    sd = []
    button = 0
    
    def __init__(self, smallblind, bigblind, maxbi = bigblind * 100, bets = [], players = [], d = [], board = [], pot = 0.0):
        self.smallblind = smallblind
        self.bigblind = bigblind
        self.maxbi = maxbi
        self.bets = bets
        self.players = players
        self.d = dk.Deck()
        self.board = board
        self.button = 0
        self.pot = pot

    def bettinground(self, preflop = False):
        i = 0
        seatact= -1
        firstbet = True
        origbet = max(self.bets)
        if preflop == True:
            poscloseaction = self.button + 3
        else:
            poscloseaction = self.button + 1
        if poscloseaction >= len(self.players):
            poscloseaction = poscloseaction - len(self.players)
        while seatact != poscloseaction:
            if i == 0:
                seatact = poscloseaction
                i = 1
            if (self.players[seatact].hand != []) | (self.players[seatact].stack == 0.0):
                for i in range(len(self.players)):
                    self.players[i].pot = self.pot
                    self.players[i].bets = self.bets
                    self.players[i].board = self.board
                self.players[seatact].act = ''
                while (self.players[seatact].act != 'check/fold') & (self.players[seatact].act != 'call') & (self.players[seatact].act != 'bet/raise') & (self.players[seatact].act != 'allin'):
                    self.players[seatact].action()
                    if self.players[seatact].act == 'bet/raise':
                        while (self.players[seatact].betamt > self.players[seatact].stack) | (self.players[seatact].betamt < 2.0) | ((origbet != 0.0) & (self.players[seatact].betamt < origbet * 2)):
                            self.players[seatact].action()
                            if self.players[seatact].act == 'bet/raise':
                                if self.players[seatact].betamt > self.players[seatact].stack:
                                    self.players[seatact].error = 'stack too small'
                                elif self.players[seatact].betamt < 2.0:
                                    self.players[seatact].error = 'min bet is at least a big blind'
                                elif (origbet != 0.0) & (self.players[seatact].betamt < origbet * 2):
                                    self.players[seatact].error = 'raise must be at least double original bet'
                            else:
                                break
                        if firstbet == True:
                            firstbet = False
                            origbet = self.players[seatact].betamt
                        self.players[seatact].stack = self.players[seatact].stack - self.players[seatact].betamt + self.bets[seatact]
                        self.bets[seatact] = self.players[seatact].betamt
                        poscloseaction = seatact
                    elif (self.players[seatact].act == 'allin'):
                        self.players[seatact].betamt = self.players[seatact].stack
                        self.bets[seatact] = self.players[seatact].stack
                        self.players[seatact].stack = 0
                    elif (self.players[seatact].act == 'check/fold') & (self.bets[seatact] != max(self.bets)):
                        self.players[seatact].hand = []
                    elif self.players[seatact].act == 'call':
                        self.players[seatact].stack = self.players[seatact].stack - max(self.bets) + self.bets[seatact]
                        self.bets[seatact] = max(self.bets)
                        
                print('\n', self.players[seatact].name, 'stack:', self.players[seatact].stack)
                print(self.players[seatact].act, self.bets[seatact])
                print(self.bets)
            seatact = seatact + 1
            if seatact == len(self.players):
                seatact = 0
        self.pot = self.pot + sum(self.bets)
        print('pot', self.pot)
        self.bets = [num * 0 for num in self.bets]
        if sum([i != [] for i in [j.hand for j in self.players]]) == 1:
            if self.endhand():
                return True

    def endhand(self):
        winner = []
        if sum([i != [] for i in [j.hand for j in self.players]]) == 1:
            winner.append([i != [] for i in [j.hand for j in self.players]].index(True))
        else:
            winarray = calculate.equity(self.board, [i.hand for i in self.players])
            print(winarray)
            if [1.0, 0.0] in winarray:
                winner.append([i == [1.0, 0.0] for i in winarray].index(True))
            else:
                for i in range(len(winarray)):
                    if (winarray[i] == [0.0, 1.0]) & (self.players[i].hand != []):
                        winner.append(i)
            print(winner)

        for w in winner:
            print('winner:', self.players[w].name, self.players[w].hand, self.board)
            print('wins:', self.pot/len(winner))
            self.players[w].stack = self.players[w].stack + self.pot/len(winner)
        print('________________________________\n\n\n')
        self.bets = []
        self.board = []
        self.d.__init__()
        self.d.shuffle()
        self.button = self.button + 1
        if self.button >= len(self.players):
            self.button = 0
        for i in range(len(self.players)):
            self.players[i].pot = self.pot
            self.players[i].bets = self.bets
            self.players[i].board = self.board
            self.players[i].reload()
        return True;

    def nlhhand(self):
        self.pot = 0.0
        self.bets = []
        self.board = []
        self.d.__init__()
        self.d.shuffle()
        print('button:', self.button)

        for i in range(len(self.players)):
            self.players[i].hand = list([])
            self.d.draw(self.players[i].hand, 2)
            if (i == self.button + 1) | (i == self.button + 1 - len(self.players)):
                self.bets.append(1.0)
                self.players[i].stack = self.players[i].stack - 1.0
            elif (i == self.button + 2) | (i == self.button + 2 - len(self.players)):
                self.bets.append(2.0)
                self.players[i].stack = self.players[i].stack - 2.0
            else:
                self.bets.append(0.0)
            print(self.players[i].name, 'hand:', self.players[i].hand)
        print('\n\n\n HANDS ABOVE NO LOOKING\n------------------')
        for i in range(len(self.players)):
            print(self.players[i].name, 'stack:', self.players[i].stack)
            print(self.players[i].name, 'rebuy:', self.players[i].debt)

        if self.bettinground(preflop = True):
            return
        print(' ')

        self.d.draw(self.board, 3)
        print('flop: ', self.board)
        if self.bettinground():
            return
        print(' ')

        self.d.draw(self.board)
        print('turn: ', self.board)
        if self.bettinground():
            return
        print(' ')

        self.d.draw(self.board)
        print('river: ', self.board)
        if self.bettinground():
            return
        print(' ')
        
        self.endhand()
        
        
    def newplayer(self, name, buyin):
        _ = pl.Player(name, buyin, list([]))
        return _

player1 = mk.Mackerel('blub', 200.0, list([]))
player2 = mk.Mackerel('blug', 200.0, list([]))
player3 = mk.Mackerel('blop', 200.0, list([]))
player4 = mk.Mackerel('glub', 200.0, list([]))
player5 = mk.Mackerel('glug', 200.0, list([]))
player6 = pl.Player('Vince', 200.0, list([]))

table1 = Table(1.0,2.0)
table1.players.append(player1)
table1.players.append(player2)
table1.players.append(player3)
table1.players.append(player4)
table1.players.append(player5)
table1.players.append(player6)

for i in range(1000):
    table1.nlhhand()

#print(table1.players[0].hand)
#print(table1.players[1].hand)
#print(table1.players[2].hand)

#print(hr.handranker(table1.players[0].hand + table1.board))
#print(hr.handranker(table1.players[1].hand + table1.board))
#print(hr.handranker(table1.players[2].hand + table1.board))

#for _ in range(100):
#    table1.nlhhand()
