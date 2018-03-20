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
import deck as dk
import handrank as hr

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
    
    def __init__(self, smallblind, bigblind, maxbi = bigblind * 100, bets = [], players = [], d = [], hands = [], board = [], pot = 0.0):
        self.smallblind = smallblind
        self.bigblind = bigblind
        self.maxbi = maxbi
        self.bets = bets
        self.players = players
        self.d = dk.Deck()
        self.board = board
        self.hands = hands
        self.button = 0;
        self.pot = pot;
    
    def nlhhand(self):
        self.board = []
        self.d.__init__()
        self.d.shuffle()
        print('button:', self.button)

        for i in range(len(self.players)):
            self.players[i].hand = list([])
            self.d.draw(self.players[i].hand, 2)
            self.hands.append(self.players[i].hand)
            if i == self.button + 1:
                self.bets.append(1.0)
                self.players[i].stack = self.players[i].stack - 1.0
            elif i == self.button + 2:
                self.bets.append(2.0)
                self.players[i].stack = self.players[i].stack - 2.0
            else:
                self.bets.append(0.0)
            print(self.players[i].name, 'hand:', self.players[i].hand)
            print(self.players[i].name, 'stack:', self.players[i].stack)
        origbet = max(self.bets);
        for i in range(len(self.players)):
            self.players[i].action(origbet)

        self.pot = sum(self.bets)
        print(' ')

        self.d.draw(self.board, 3)
        print('flop: ', self.board)
        for player in self.players:
            print(player.name, calculate.handpercentile(player.hand, self.board))
        print(' ')
        self.d.draw(self.board)
        print('turn: ', self.board)
        for player in self.players:
            print(player.name, calculate.handpercentile(player.hand, self.board))
        print(' ')
        self.d.draw(self.board)
        print('river: ', self.board)
        for player in self.players:
            print(player.name, calculate.handpercentile(player.hand, self.board))
        print(' ')
#        for player in self.players:
#            if hr.handranker(hr.cardstobit(player.hand + table1.board))[0] == hr.showdown(hr.cardstobit(self.sd)):
#                print('winner:',player.name, player.hand)
        self.button = self.button + 1
        if self.button >= len(self.players):
            self.button = 0


        print('winner:', calculate.equity(self.board, self.hands))
        
        
    def newplayer(self, name, buyin):
        _ = pl.Player(name, buyin, list([]))
        return _

player1 = pl.Player('blub', 200.0, list([]))
player2 = pl.Player('blug', 200.0, list([]))
player3 = pl.Player('blop', 200.0, list([]))
player4 = pl.Player('glub', 200.0, list([]))
player5 = pl.Player('glug', 200.0, list([]))
player6 = pl.Player('glop', 200.0, list([]))

table1 = Table(1.0,2.0)
table1.players.append(player1)
table1.players.append(player2)
table1.players.append(player3)
table1.players.append(player4)
table1.players.append(player5)
table1.players.append(player6)

table1.nlhhand()

print(calculate.equity(table1.board, table1.hands))

table1.nlhhand()

print(calculate.equity(table1.board, table1.hands))

#print(table1.players[0].hand)
#print(table1.players[1].hand)
#print(table1.players[2].hand)

#print(hr.handranker(table1.players[0].hand + table1.board))
#print(hr.handranker(table1.players[1].hand + table1.board))
#print(hr.handranker(table1.players[2].hand + table1.board))

#for _ in range(100):
#    table1.nlhhand()


