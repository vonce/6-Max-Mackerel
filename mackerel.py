import os
import tools

class Mackerel(object):
    name = ''
    hand = []
    stack = 0.0

    def __init__(self, name, stack, hand, act='', betamt=0.0, board = [], pot = 0.0, bets = [], debt = 0.0, error = '', pos = 0):
        self.name = name
        self.stack = stack
        self.hand = hand
        self.act = act
        self.betamt = 0.0
        self.error = error
        self.debt = debt
        self.pos = pos

    def action(self, origbetbehind=0.0):
        
        self.act = ''
        self.betamt = 0.0 
        
        if self.board == []:
            if (tools.startinghandsrank(self.hand) > 1/2) & (max(self.bets) == 2):
                self.betamt = max(self.bets) * 3
                self.act = 'bet/raise'
            elif (tools.startinghandsrank(self.hand) > 0.90) & (max(self.bets) < self.pot):
                self.betamt = max(self.bets) * 3
                self.act = 'bet/raise'
            elif (tools.startinghandsrank(self.hand) > 1/2) & (max(self.bets) > 2):
                self.act = 'call'
            else:
                self.act = 'check/fold'
        else:
            if self.stack < 2.0:
                self.act = 'call'
            elif (calculate.handpercentile(self.hand, self.board) > 3/5) & (max(self.bets) == 0):
                if self.stack < self.pot:
                    self.betamt = self.stack
                else:
                    self.betamt = self.pot
                self.act = 'bet/raise'
            elif (calculate.handpercentile(self.hand, self.board) > 0.90) & (max(self.bets) < self.pot):
                if self.stack < self.pot:
                    self.betamt = self.stack
                if max(self.bets) == 0:
                    self.betamt = self.pot
                if max(self.bets) > self.pot/2:
                    self.betamt = max(self.bets) * 3
                else:
                    self.betamt = max(self.bets) * 5
                self.act = 'bet/raise'
            elif (calculate.handpercentile(self.hand, self.board) > 3/5) & (max(self.bets) > self.pot/2):
                self.act = 'call'
            else:
                self.act = 'check/fold' 
        if self.error != '':
            print(self.error)
            if self.error == 'stack too small':
                self.act = 'allin'
                self.betamt = self.stack
                self.stack = 0.0
            elif self.error == 'min bet is at least a big blind':
                self.betamt = self.betamt + 2
            elif self.error == 'raise must be at least double original bet':
                self.act = 'call'
            self.error = ''
        
    def reload(self):
        if self.stack < 200.0:
            self.debt = self.debt - (200 - self.stack)
            self.stack = 200.0

