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
import os
import timeit

def extract(txt):
    filename = txt
    file = open(txt)
    
    lines = file.readlines()
    file.close()
    
    allgames = []
    y = ''
    for line in lines:
        y = y + line
        if 'Game ended at:' in line:
            allgames.append(y)
            y = ''
    games = []
    
    for i in range(len(allgames)):    
        allgames[i] = allgames[i].replace('?','')
        
    for game in allgames:
        if 'shows:' in game:
            games.append(game)

    df = []
    vpippfrplayers = []

    vpip = []
    pfr = []
    for game in allgames:
        vpippfrplayers = vpippfrplayers + re.findall('Seat\s\d:\s(.+)\s\(', game)
    vpippfrplayers = list(set(vpippfrplayers))
    vpippfrdf = pd.DataFrame(vpippfrplayers, columns = ['name'])
    vpippfrdf['tot option'] = 0
    vpippfrdf['tot put in pot'] = 0
    vpippfrdf['tot preflop raise'] = 0

    for game in allgames:
        if '*** FLOP ***' in game: 
            pfstring = game[(game.index('Game started at:')+len('Game started at:')):game.index('*** FLOP ***')]
        else:
            pfstring = game[:game.index('------ Summary ------')]

        vpippfrcount = re.findall('Player\s(.+)\sraises|Player\s(.+)\sallin|Player\s(.+)\scalls|Player\s(.+)\schecks|Player\s(.+)\sfolds', pfstring)
        for i in vpippfrcount:
            for j in i:
                if j != '':
                    vpipname = j
            vpippfrdf.loc[vpippfrdf['name'] == vpipname, 'tot option'] += 1
            if (i[0] != '')|(i[1] != '')|(i[2] != ''):
                vpippfrdf.loc[vpippfrdf['name'] == vpipname, 'tot put in pot'] += 1
            if (i[0] != '')|(i[1] != ''):
                vpippfrdf.loc[vpippfrdf['name'] == vpipname, 'tot preflop raise'] += 1
    vpippfrdf['vpip'] = vpippfrdf['tot put in pot']/vpippfrdf['tot option']
    vpippfrdf['pfr'] = vpippfrdf['tot preflop raise']/vpippfrdf['tot option']
    for game in games:
        names = re.findall('Player\s(.*?)\sshows:', game)
        cards = re.findall('Player\s.*?\sshows:.+\[(.*?)\]', game)
        actions = []
        
        board = re.search('Board:\s\[(.+)\]', game)
        if board:
            board = board.group(1)
            board = board.replace('10','T')
            board = board.split(' ')
            board = hr.convert(board)
        for i in range(len(cards)):
            cards[i] = cards[i].replace('10','T')
            cards[i] = cards[i].split(' ')
            cards[i] = hr.convert(cards[i])
            
    
        bigblind = float(re.search('Game ID:\s.+\/([\d.]+)\s', game).group(1))   
        stacks = []
        
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
        streetreached = 0
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
            if re.findall('Player\s(.+)\s', flstring) != []:
                streetreached = 1
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
            if re.findall('Player\s(.+)\s', trstring) != []:
                streetreached = 2
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
            if re.findall('Player\s(.+)\s', rvstring) != []:
                streetreached = 3
            
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
            vpip = float(vpippfrdf.loc[vpippfrdf['name'] == names[i], 'vpip'].get_values())         
            pfr = float(vpippfrdf.loc[vpippfrdf['name'] == names[i], 'pfr'].get_values())
            
            if board:
                if len(board) == 5:    
                    handstrengthrv = hr.handrankboard(cards[i], board)
                if len(board) >= 4:    
                    handstrengthtr = hr.handrankboard(cards[i], board[:4])
                    drawstr = hr.draws(cards[i], board[:4])
                if len(board) >= 3:    
                    handstrengthfl = hr.handrankboard(cards[i], board[:3])
                    drawsfl = hr.draws(cards[i], board[:3])
            stacks = float(re.search(names[i] + '\s\((.*?)\)', game).group(1))   
            actions = re.findall(names[i] + '\s(.+)\s\(([\d\.]+)\)|' + names[i] + '\s(checks)|\*\*\*\s(\w+)\s\*\*\*|--\s(Summary)\s--|Uncalled\sbet\s\(([\d\.]+)\)\sreturned\sto\s' + names[i], game)
            bets = 0.0
            allbets = []
            agg = 0
            allagg = []
            blufffl = 0
            blufftr = 0
            bluffrv = 0
            street = ''
            for action in actions:
                if (action[3] == 'FLOP')|(action[3] == 'TURN')|(action[3] == 'RIVER')|(action[4] == 'Summary'):
                    allbets.append(round(bets, 2))
                    allagg.append(agg)
                    bets = 0.0
                    agg = 0.0
                    if action[3] == 'FLOP':
                        street = action[3]
                    if action[3] == 'TURN':
                        street = action[3]
                    if action[3] == 'RIVER':
                        street = action[3]
                else:             
                    if (action[1] != ''):
                        bets = bets + float(action[1])  
                    if (action[5] != ''):
                        bets = bets - float(action[5])
                    if (action[0] == 'raises'):
                        agg = agg + float(action[1])
                    if (action[0] == 'bets'):
                        agg = agg + float(action[1])
                    if (action[0] == 'allin'):
                        agg = agg + float(action[1])
                    
                    
                    if (street == 'FLOP') & ((action[0] == 'raises')|(action[0] == 'bets')|(action[0] == 'allin')) & (handstrengthfl < .6):
                        blufffl = 1
                    if (street == 'TURN') & ((action[0] == 'raises')|(action[0] == 'bets')|(action[0] == 'allin')) & (handstrengthtr < .6):
                        blufftr = 1
                    if (street == 'RIVER') & ((action[0] == 'raises')|(action[0] == 'bets')|(action[0] == 'allin')) & (handstrengthrv < .6):
                        bluffrv = 1
            for j in range(3):
                if len(allbets) < 4:
                    allbets.append(0.0)
            for j in range(3):
                if len(allagg) < 4:
                    allagg.append(0)
                
            data = [filename, # filename
                    names[i],#name(str)
                    vpip,#vpip
                    pfr,#pfr
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
                    handstrengthfl,# hand strength flop
                    blufffl, # bluff flop
                    drawsfl[0], #flush draws flop
                    drawsfl[1], #straight draws flop
                    drawsfl[2], #straight flush draws flop
                    round((stacks - allbets[0] - allbets[1])/bigblind, 2),# stack GOING INTO turn
                    pltr,# # players GOING INTO turn
                    playerstr.index(names[i]),# position turn
                    playerstr.index(names[i])/(pltr - 1),# position turn/total players
                    round(allbets[2]/bigblind, 2),#turn bets in (bb)
                    round(allbets[2]/flpot, 2),#turn bets/flpot
                    allagg[2],# turn aggression
                    round((stacks - allbets[0] - allbets[1] - allbets[2])/trpot, 2),#stack/turn pot
                    handstrengthtr,# hand strength turn
                    blufftr, #bluff turn
                    drawstr[0], #flush draws turn
                    drawstr[1], #straight draws turn
                    drawstr[2], #straight flush draws turn
                    round((stacks - allbets[0] - allbets[1] - allbets[2])/bigblind, 2),# stack GOING INTO river
                    plrv,# # players GOING INTO river
                    playersrv.index(names[i]),# position river
                    playersrv.index(names[i])/(plrv - 1),# position river/total players
                    round(allbets[3]/bigblind, 2),#river bets in (bb)
                    round(allbets[3]/pfpot, 2),# river bets/trpot
                    allagg[3],# river aggression
                    round((stacks - allbets[0] - allbets[1] - allbets[2] - allbets[3])/rvpot, 2),#stack/river pot
                    handstrengthrv,#hand strength river
                    bluffrv,# bluff river
                    sum(allbets),# total bets
                    sum(allagg),#total aggression
                    round(sum(allbets)/stacks, 2),#bets/stacks
                    streetreached
                    ]
            df.append(data)
            
    columnsriver = ['filename',#filename
            'name',#name(str)
            'vpip',#vpip
            'pfr',#pfr
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
           'hand strength fl',# hand strength flop
           'bluff flop',# bluff flop
           'flush draws flop',#flush draws flop
           'straight draws flop',#straight draws flop
           'straight flush draws flop',
           'tr stack(bb)',# stack GOING INTO turn
           '#pl tr',# # players GOING INTO turn
           'position tr',# position turn
           'position tr/#pl tr',# position turn/total players
           'tr bets(bb)',# turn bets in (bb)
           'tr bets/pot',# turn bets/flpot
           'tr agg',# turn aggression
           'stack/trpot',# stack/turn pot
           'hand strength tr',# hand strength turn
           'bluff turn',# bluff turn
           'flush draws turn',#flush draws flop
           'straight draws turn',#straight draws flop  
           'straight flush draws turn',
           'rv stack(bb)',#stack GOING INTO river
           '#pl rv',# # players GOING INTO river
           'position rv',# position river
           'position rv/#pl rv',# position river/total players
           'rv bets(bb)',# river bets in (bb)
           'rv bets/pot',#river bets/ trpot
           'rv agg',# river aggression
           'stack/rvpot',# stack/ river pot
           'hand strength rv',# hand strength river
           'bluff river',# bluff river
           'tot bets',# total bets
           'tot agg',# total aggression
           'bets/stacks',# bets/stacks
           'street reached'# street reached
           ]    
    df = pd.DataFrame(df, columns = columnsriver)
    return df

alldata = []
for filename in os.listdir('data'):
    start = timeit.default_timer()
    if filename.endswith('.txt'): 
        print('reading:' + filename)
        alldata.append(extract('data/' + filename))
        stop = timeit.default_timer()
        print('Done reading' + filename + 'in' +(start-stop) + 's')
alldata = pd.concat(alldata)
alldata.to_csv('data.csv')

