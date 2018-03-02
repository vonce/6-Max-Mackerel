#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 11:57:57 2018

@author: Vince
"""

import re
import pandas as pd
import numpy as np
import handrank as hr

file = open('data/(PRR) Cyclops - 6-0.02-0.05-USD-NoLimitHoldem-WinningPoker-2-20-2018.txt')

lines = file.readlines()

file.close()
#print(lines)
games = []
y = ''
for line in lines:
        y = y + line
        if 'Game ended at:' in line:
            games.append(y)
            y = ''
i = []
for game in games:
    if 'shows:' in game:
        i.append(game)
games = i
for i in range(len(games)):    
    games[i] = games[i].replace('?','')
df = []
for game in games:
    
    names = re.findall('Player\s(.*?)\sshows:', game)
    cards = re.findall('Player\s.*?\sshows:.+\[(.*?)\]', game)
    actions = []
    
    board = re.search('Board:\s\[(.+)\]', game)
    if board:
        board = board.group(1)
        board = board.replace('10','T')
        board = board.split(' ')
    for i in range(len(cards)):
        cards[i] = cards[i].replace('10','T')
        cards[i] = cards[i].split(' ')
        

    bigblind = float(re.search('Game ID:\s.+\/([\d.]+)\s', game).group(1))   
    stacks = []
    pot = round(sum([float(i) for i in re.findall('\(([\d.]+)\)[^.][^r]', game)]), 2)
    pfpot = 0.0
    flpot = 0.0
    trpot = 0.0
    rvpot = 0.0
    button = re.search('(Seat\s\d)\sis the button', game).group(1)
    button = re.search('%s:\s(.+)\s\('% button, game).group(1)
    players = re.findall('Seat\s\d:\s(.+)\s\(',game)
    for i in range(len(players)):        
        if players[-1] != button:
            players.insert(0, players.pop(players.index(players[-1])))
    players = list(reversed(players))
    plpf = len(players)
    plfl = 0
    pltr = 0
    plrv = 0
    playerspf = players
    if '*** FLOP ***' in game: 
        pfstring = game[(game.index('Game started at:')+len('Game started at:')):game.index('*** FLOP ***')]
    else:
        pfstring = game[:game.index('------ Summary ------')]
    foldplayerspf = re.findall('Player\s(.+)\sfolds', pfstring)
    pfpot = round(sum([float(i) for i in re.findall('\(([\d.]+)\)[^.]', pfstring)]), 2)
    if '*** FLOP ***' in game:
        if '*** TURN ***' in game:
            flstring = game[(game.index('*** FLOP ***')+len('*** FLOP ***')):game.index('*** TURN ***')]
        else:
            flstring = game[(game.index('*** FLOP ***')+len('*** FLOP ***')):game.index('------ Summary ------')]
        foldplayersfl = re.findall('Player\s(.+)\sfolds', flstring)
        flpot = round(pfpot + sum([float(i) for i in re.findall('\(([\d.]+)\)[^.]', flstring)]), 2)
        playersfl = list(players)   
        for player in players:
            if player in foldplayerspf:
                playersfl.remove(player)
    else:
        flpot = pfpot
        playersfl = list(players)
    if '*** TURN ***' in game:  
        if '*** RIVER ***' in game:
            trstring = game[(game.index('*** TURN ***')+len('*** TURN ***')):game.index('*** RIVER ***')]
        else:
            trstring = game[(game.index('*** TURN ***')+len('*** TURN ***')):game.index('------ Summary ------')]
        foldplayerstr = re.findall('Player\s(.+)\sfolds', trstring)
        trpot = round(flpot + sum([float(i) for i in re.findall('\(([\d.]+)\)[^.]', trstring)]), 2)
        playerstr = list(playersfl)
        for player in playersfl:
            if player in foldplayersfl:
                playerstr.remove(player)
    else:
        trpot = flpot
        playerstr = list(playersfl)
    if '*** RIVER ***' in game:  
        rvstring = game[(game.index('*** RIVER ***')+len('*** RIVER ***')):game.index('------ Summary ------')]
        foldplayersrv = re.findall('Player\s(.+)\sfolds', rvstring)
        rvpot = round(trpot + sum([float(i) for i in re.findall('\(([\d.]+)\)[^.]', rvstring)]), 2)
        playersrv = list(playerstr)
        for player in playerstr:
            if player in foldplayerstr:
                playersrv.remove(player)
    else:
        rvpot = trpot
        playersrv = list(playerstr)
    plfl = len(playersfl)
    pltr = len(playerstr)
    plrv = len(playersrv)
    
    for i in range(len(names)):
        stacks = float(re.search(names[i] + '\s\((.*?)\)', game).group(1))   
        actions = re.findall(names[i] + '\s(.+)\s\(([\d\.]+)\)|' + names[i] + '\s(checks)|\*\*\*\s(\w+)\s\*\*\*|--\s(Summary)\s--', game)
        bets = 0.0
        allbets = []
        agg = 0
        allagg = []
        for action in actions:
            if (action[3] == 'FLOP')|(action[3] == 'TURN')|(action[3] == 'RIVER')|(action[4] == 'Summary'):
                allbets.append(round(bets, 2))
                allagg.append(agg)
                bets = 0.0
                agg = 0
            else:               
                if action[1] != '':
                    bets = bets + float(action[1])
                    
                if (action[0] == 'raises'):
                    agg = agg + 2
                if (action[0] == 'bets'):
                    agg = agg + 1
                if (action[0] == 'allin'):
                    agg = agg + 1
        for j in range(3):
            if len(allbets) < 4:
                allbets.append(0.0)
        for j in range(3):
            if len(allagg) < 4:
                allagg.append(0)

#        print('pot', pot)
#        print('players pf', plpf)
#        print(playerspf)
#        print('pf pot', pfpot)
#        print('players fl', plfl)
#        print(playersfl)
#        print('fl pot', flpot)
#        print('players tr', pltr)
#        print(playerstr)
#        print('tr pot', trpot)
#        print('players rv', plrv)
#        print(playersrv)
#        print('rv pot', rvpot)
#        print(allagg)
#        print('bb', bigblind)
#        print('all bets', allbets)
#        print('name', names[i])
#        print('hand', cards[i])
#        if board:
#            print('board', board)
#        print('stack', stacks)
#        print(actions)
#        print(round(stacks/bigblind, 2))
#        print('')
        
        data = [names[i],#name(str)
                cards[i],#hand[(str),(str)]
                board,#board[strings]
                round(stacks/bigblind, 2),#preflop stack in bigblinds
                plpf,# #players preflop
                playerspf.index(names[i]),#player's position preflop, 0 is button
                playerspf.index(names[i])/(plpf - 1),#player's position preflop/total players
                round(allbets[0]/bigblind, 2),#preflop bets in (bb)
                allagg[0],# preflop aggression
                round((stacks - allbets[0])/pfpot, 2),# stack/preflop pot
                round((stacks - allbets[0])/bigblind, 2),# stack GOING INTO flop
                plfl,# # players GOING INTO flop
                playersfl.index(names[i]),# position flop
                playersfl.index(names[i])/(plfl - 1),# position flop/total players
                round(allbets[1]/bigblind, 2),#flop bets in (bb)
                round(allbets[1]/pfpot, 2),# flop bets/pfpot
                allagg[1],# flop aggression
                round((stacks - allbets[0] - allbets[1])/flpot, 2),#stack/flop pot
                round((stacks - allbets[0] - allbets[1])/bigblind, 2),# stack GOING INTO turn
                pltr,# # players GOING INTO turn
                playerstr.index(names[i]),# position turn
                playerstr.index(names[i])/(pltr - 1),# position turn/total players
                round(allbets[2]/bigblind, 2),#turn bets in (bb)
                round(allbets[2]/flpot, 2),#turn bets/flpot
                allagg[2],# turn aggression
                round((stacks - allbets[0] - allbets[1] - allbets[2])/trpot, 2),#stack/turn pot
                round((stacks - allbets[0] - allbets[1] - allbets[2])/bigblind, 2),# stack GOING INTO river
                plrv,# # players GOING INTO river
                playersrv.index(names[i]),# position river
                playersrv.index(names[i])/(plrv - 1),# position river/total players
                round(allbets[3]/bigblind, 2),#river bets in (bb)
                round(allbets[3]/pfpot, 2),# river bets/trpot
                allagg[3],# river aggression
                round((stacks - allbets[0] - allbets[1] - allbets[2] - allbets[3])/rvpot, 2),#stack/river pot
                sum(allbets),# total bets
                sum(allagg)#total aggression
                ]
        df.append(data)
columnsriver = ['name',#name(str)
           'hand', #hand[(str),(str)]
           'board',#board[strings]
           'pf stack(bb)',#preflop stack in big blinds
           '#pl pf',# #players preflop
           'position pf',#player's position preflop, 0 is button
           'position pf/#pl pf',# player's position preflop/total players
           'pf bets(bb)',# preflop bets in (bb)
           'pf agg',# preflop aggression
           'stack/pfpot',# stack/preflop pot
           'fl stack(bb)',# stack GOING INTO flop
           '#pl fl',# #players GOING INTO flop
           'position fl',# position flop
           'position fl/#pl fl',# position flop/total players
           'fl bets(bb)',# flop bets in (bb) 
           'fl bets/pot',# flop bets/pfpot
           'fl agg',# flop aggression
           'stack/flpot',# stack/flop pot
           'tr stack(bb)',# stack GOING INTO turn
           '#pl tr',# # players GOING INTO turn
           'position tr',# position turn
           'position tr/#pl tr',# position turn/total players
           'tr bets(bb)',# turn bets in (bb)
           'tr bets/pot',# turn bets/flpot
           'tr agg',# turn aggression
           'stack/trpot',# stack/turn pot
           'rv stack(bb)',#stack GOING INTO river
           '#pl rv',# # players GOING INTO river
           'position rv',# position river
           'position rv/#pl rv',# position river/total players
           'rv bets(bb)',# river bets in (bb)
           'rv bets/pot',#river bets/ trpot
           'rv agg',# river aggression
           'stack/rvpot',# stack/ river pot
           'tot bets',# total bets
           'tot agg',# total aggression
]
handstrength = []
df = pd.DataFrame(df, columns = columnsriver)
df['hand'] = df['hand'].apply(hr.convert)
df['board'] = df['board'].apply(hr.convert)
for row in range(len(df['hand'])):
    hs = hr.handrankboard(df['hand'][row], df['board'][row])
    handstrength.append(hs)
    print('row', row, 'complete:', hs)

handstrength = pd.Series(handstrength)
df.loc[:,'hand strength'] = handstrength
print(df)