class Mackerel(object):
    name = ''
    hand = []
    stack = 0.0

    def __init__(self, name, stack, hand, act='', betamt=0.0):
        self.name = name
        self.stack = stack
        self.hand = hand
        self.act = act
        self.betamt = 0.0

    def action(self, origbetbehind=0.0):
        self.act = 'call'
#        print(self.name, 'action: ', 'check/fold', 'bet/raise', 'call?')
#        self.act = ''
#        self.betamt = 0.0
#        while (self.act != 'check/fold') & (self.act != 'bet/raise') & (self.act != 'call'):
#            self.act = input(':')
#        if self.act == 'bet/raise':
#            while (self.betamt > self.stack) | (self.betamt < 2.0) | (
#                    (origbetbehind != 0.0) & (self.betamt < origbetbehind * 2)):
#                self.betamt = float(input('amount:'))
#                if self.betamt > self.stack:
#                    print('stack too small')
#                if self.betamt < 2.0:
#                    print('min bet is at least a big blind')
#                if (origbetbehind != 0.0) & (self.betamt < origbetbehind * 2):
#                    print('raise must be at least double original bet')

