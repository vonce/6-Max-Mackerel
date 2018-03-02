#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 19:01:19 2018

@author: Vince
"""
import player as pl
import deck as dk
import handrank as hr
import numpy as np

class Table(object):
    players = []
    bigblind = 0.0
    bets = []
    pot = 0.0
    d = []
    board = []
    sd = []
    def __init__(self, smallblind, bigblind, maxbi = bigblind * 100, players = [], d = [], board = [], sd = []):
        self.smallblind = smallblind
        self.bigblind = bigblind
        self.maxbi = maxbi
        self.players = players
        self.d = dk.Deck()
        self.board = board
        self.sd = sd
    
    def nlhhand(self):
        self.board = []
        self.sd = []
        self.d.__init__()
        self.d.shuffle()

        for player in self.players:
            player.hand = list([])
            self.d.draw(player.hand, 2)
            print(player.name, player.hand)
        print(' ')
        self.d.draw(self.board, 3)
        print('flop: ', self.board)
        for player in self.players:
            print(player.name, hr.handranker(player.hand + table1.board))
        print(' ')
        self.d.draw(self.board)
        print('turn: ', self.board)
        for player in self.players:
            print(player.name, hr.handranker(player.hand + table1.board))
        print(' ')
        self.d.draw(self.board)
        print('river: ', self.board)
        for player in self.players:
            self.sd.append(hr.handranker(player.hand + table1.board))
            print(player.name, hr.handranker(player.hand + table1.board))
        print(' ')
        for player in self.players:
            if hr.handranker(player.hand + table1.board)[0] == hr.showdown(self.sd):
                print('winner:',player.name, player.hand)
#        print('winner:', hr.showdown(self.sd))
        
        
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

print(table1.players[0].name, hr.handrankboard(table1.players[0].hand, table1.board))
print(table1.players[1].name, hr.handrankboard(table1.players[1].hand, table1.board))
print(table1.players[2].name, hr.handrankboard(table1.players[2].hand, table1.board))
print(table1.players[3].name, hr.handrankboard(table1.players[3].hand, table1.board))
print(table1.players[4].name, hr.handrankboard(table1.players[4].hand, table1.board))
print(table1.players[5].name, hr.handrankboard(table1.players[5].hand, table1.board))

#print(table1.players[0].hand)
#print(table1.players[1].hand)
#print(table1.players[2].hand)

#print(hr.handranker(table1.players[0].hand + table1.board))
#print(hr.handranker(table1.players[1].hand + table1.board))
#print(hr.handranker(table1.players[2].hand + table1.board))

#for _ in range(100):
#    table1.nlhhand()


