#only works for .50/1 blinds, eventually fix for /bb
import os

os.environ['JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_161.jdk/Contents/Home"  # type which java in terminal and paste here
os.environ['CLASSPATH'] = "./Flounder.jar"
from jnius import autoclass
import re
import pandas as pd
import timeit
calculate = autoclass("flounder.Calculate")

playerlist = []
col = [
    'avgstack',
    'net',
    'foldpf',
    'callpf',
    'raisepf',
    'foldtoraisepf',
    'numraisedpf',
    'reraisepf',
    'foldtoreraisepf',
    'numreraisedpf',
    'numplayedpf',
    'pctseenfl',
    'foldfl',
    'callfl',
    'betfl',
    'raisefl',
    'foldtoraisefl',
    'numraisedfl',
    'reraisefl',
    'foldtoreraisefl',
    'numreraisedfl',
    'numplayedfl',
    'pctseentr',
    'foldtr',
    'calltr',
    'bettr',
    'raisetr',
    'foldtoraisetr',
    'numraisedtr',
    'reraisetr',
    'foldtoreraisetr',
    'numreraisedtr',
    'numplayedtr',
    'pctseenrv',
    'foldrv',
    'callrv',
    'betrv',
    'raiserv',
    'foldtoraiserv',
    'numraisedrv',
    'reraiserv',
    'foldtoreraiserv',
    'numreraisedrv',
    'numplayedrv',
    'pctseensd',
    'numplayedsd',
    'winpercent'
]
df = pd.DataFrame(columns = col)
print(df)
def extractstat(txt):  # extracts stats from Winning Poker Network datamined data.

    file = open(txt)
    global df
    global playerlist
    lines = file.readlines()
    file.close()
    allgames = []
    y = ''
    for line in lines:
        y = y + line
        if 'Game ended at:' in line:
            allgames.append(y)
            y = ''

    for i in range(len(allgames)):
        allnames = re.findall('Seat [\d]: (.*) \(', allgames[i])
        newnames = list(allnames)
        for j in range(len(allnames)):
            for char in ['_', '[', '\\', '^', '$', '.', '|', '?', '*', '+', '(', ')']:
                if char in allnames[j]:
                    newnames[j] = newnames[j].replace(char, '`')
        for j in range(len(allnames)):
            allgames[i] = allgames[i].replace(allnames[j], newnames[j])
        playerlist = playerlist + newnames
        playerlist = list(set(playerlist))

    for player in playerlist:
        if player not in list(df.index.values):
            tempdf = pd.DataFrame(0, index = [player], columns = col)
            df = df.append(tempdf)

    for game in allgames:
        names = re.findall('Seat [\d]: (.*) \(', game)
        stacks = re.findall('Seat [\d]: .* \((.*)\)', game)
        stacks = [float(stack) for stack in stacks]
        pfstring = ''
        flstring = ''
        trstring = ''
        rvstring = ''

        if '*** FLOP ***' in game:
            pfstring = game[(game.index('Game started at:') + len('Game started at:')):game.index('*** FLOP ***')]
        else:
            pfstring = game[:game.index('------ Summary ------')]
        if '*** FLOP ***' in game:
            if '*** TURN ***' in game:
                flstring = game[(game.index('*** FLOP ***') + len('*** FLOP ***')):game.index('*** TURN ***')]
            else:
                flstring = game[(game.index('*** FLOP ***') + len('*** FLOP ***')):game.index('------ Summary ------')]
        if '*** TURN ***' in game:
            if '*** RIVER ***' in game:
                trstring = game[(game.index('*** TURN ***') + len('*** TURN ***')):game.index('*** RIVER ***')]
            else:
                trstring = game[(game.index('*** TURN ***') + len('*** TURN ***')):game.index('------ Summary ------')]
        if '*** RIVER ***' in game:
            rvstring = game[(game.index('*** RIVER ***') + len('*** RIVER ***')):game.index('------ Summary ------')]

        summstring = game[(game.index('------ Summary ------') + len('------ Summary ------')):]

        foldpf = re.findall('Player (.*) folds', pfstring)
        callpf = re.findall('Player (.*) calls', pfstring)
        raisepf = re.findall('Player (.*) raises', pfstring)
        allinpf = re.findall('Player (.*) allin', pfstring)
        if len(list(allinpf)) > 1:
            callpf = callpf + allinpf[:len(allinpf) - 1]
        if allinpf:
            raisepf = raisepf + [allinpf[-1]]

        foldfl = re.findall('Player (.*) folds', flstring)
        callfl = re.findall('Player (.*) calls', flstring)
        betfl = re.findall('Player (.*) bets', flstring)
        raisefl = re.findall('Player (.*) raises', flstring)
        allinfl = re.findall('Player (.*) allin', flstring)
        if len(list(allinfl)) > 1:
            callfl = callfl + allinfl[:len(allinfl) - 1]
        if allinfl:
            raisefl = raisefl + [allinfl[-1]]

        foldtr = re.findall('Player (.*) folds', trstring)
        calltr = re.findall('Player (.*) calls', trstring)
        bettr = re.findall('Player (.*) bets', trstring)
        raisetr = re.findall('Player (.*) raises', trstring)
        allintr = re.findall('Player (.*) allin', trstring)
        if len(list(allintr)) > 1:
            calltr = calltr + allintr[:len(allintr) - 1]
        if allintr:
            raisetr = raisetr + [allintr[-1]]
            
        foldrv = re.findall('Player (.*) folds', rvstring)
        callrv = re.findall('Player (.*) calls', rvstring)
        betrv = re.findall('Player (.*) bets', rvstring)
        raiserv = re.findall('Player (.*) raises', rvstring)
        allinrv = re.findall('Player (.*) allin', rvstring)
        if len(list(allinrv)) > 1:
            callrv = callrv + allinrv[:len(allinrv) - 1]
        if allinrv:
            raiserv = raiserv + [allinrv[-1]]
        
        seensd = re.findall('Player (.*) shows', summstring)
        seensd = seensd + re.findall('Player (.*) mucks', summstring)
            
        win = re.findall('\*Player (.*) mucks', summstring)
        win = win + re.findall('\*Player (.*) shows', summstring)

        for i in range(len(names)):
            netplus = re.findall('Player ' + names[i] + '.* Wins: (.*)\.', summstring)
            if  netplus != []:
                df.at[names[i], 'net'] = df.at[names[i], 'net'] + float(netplus[0])
            netminus = re.findall('Player ' + names[i] + '.* Loses: (.*)\.', summstring)
            if  netminus != []:
                df.at[names[i], 'net'] = df.at[names[i], 'net'] - float(netminus[0])
                    
            if names[i] in win:
                df.at[names[i], 'winpercent'] = df.at[names[i], 'winpercent'] + 1
            df.at[names[i], 'avgstack'] = df.at[names[i], 'avgstack'] + stacks[i]
            df.at[names[i], 'numplayedpf'] = df.at[names[i], 'numplayedpf'] + 1
            if names[i] in foldpf:
                df.at[names[i], 'foldpf'] = df.at[names[i], 'foldpf'] + 1
            if raisepf:
                if ((len(raisepf) >= 1) & (raisepf[-1] != names[i])):
                    df.at[names[i], 'numraisedpf'] = df.at[names[i], 'numraisedpf'] + 1
                if ((len(raisepf) >= 1) & (names[i] in foldpf)):
                    df.at[names[i], 'foldtoraisepf'] = df.at[names[i], 'foldtoraisepf'] + 1
            if names[i] in callpf:
                df.at[names[i], 'callpf'] = df.at[names[i], 'callpf'] + 1
            if names[i] in raisepf:
                df.at[names[i], 'raisepf'] = df.at[names[i], 'raisepf'] + 1
                if ((len(raisepf) > 1) & (raisepf[-1] == names[i])):
                    df.at[names[i], 'reraisepf'] = df.at[names[i], 'reraisepf'] + 1
                if ((len(raisepf) > 1) & (raisepf[-1] != names[i])):
                    df.at[names[i], 'numreraisedpf'] = df.at[names[i], 'numreraisedpf'] + 1
                if ((len(raisepf) > 1) & (names[i] in foldpf)):
                    df.at[names[i], 'foldtoreraisepf'] = df.at[names[i], 'foldtoreraisepf'] + 1

            if flstring:
                if names[i] in flstring:
                    df.at[names[i], 'numplayedfl'] = df.at[names[i], 'numplayedfl'] + 1
                if names[i] in foldfl:
                    df.at[names[i], 'foldfl'] = df.at[names[i], 'foldfl'] + 1
                if raisefl:
                    if ((len(raisefl) >= 1) & (raisefl[-1] != names[i])):
                        df.at[names[i], 'numraisedfl'] = df.at[names[i], 'numraisedfl'] + 1
                    if ((len(raisefl) >= 1) & (names[i] in foldfl)):
                        df.at[names[i], 'foldtoraisefl'] = df.at[names[i], 'foldtoraisefl'] + 1
                if names[i] in callfl:
                    df.at[names[i], 'callfl'] = df.at[names[i], 'callfl'] + 1
                if names[i] in betfl:
                    df.at[names[i], 'betfl'] = df.at[names[i], 'betfl'] + 1
                if names[i] in raisefl:
                    df.at[names[i], 'raisefl'] = df.at[names[i], 'raisefl'] + 1
                    if ((len(raisefl) > 1) & (raisefl[-1] == names[i])):
                        df.at[names[i], 'reraisefl'] = df.at[names[i], 'reraisefl'] + 1
                    if ((len(raisefl) > 1) & (raisefl[-1] != names[i])):
                        df.at[names[i], 'numreraisedfl'] = df.at[names[i], 'numreraisedfl'] + 1
                    if ((len(raisefl) > 1) & (names[i] in foldfl)):
                        df.at[names[i], 'foldtoreraisefl'] = df.at[names[i], 'foldtoreraisefl'] + 1

            if trstring:
                if names[i] in trstring:
                    df.at[names[i], 'numplayedtr'] = df.at[names[i], 'numplayedtr'] + 1
                if names[i] in foldtr:
                    df.at[names[i], 'foldtr'] = df.at[names[i], 'foldtr'] + 1
                if raisetr:
                    if ((len(raisetr) >= 1) & (raisetr[-1] != names[i])):
                        df.at[names[i], 'numraisedtr'] = df.at[names[i], 'numraisedtr'] + 1
                    if ((len(raisetr) >= 1) & (names[i] in foldtr)):
                        df.at[names[i], 'foldtoraisetr'] = df.at[names[i], 'foldtoraisetr'] + 1
                if names[i] in calltr:
                    df.at[names[i], 'calltr'] = df.at[names[i], 'calltr'] + 1
                if names[i] in bettr:
                    df.at[names[i], 'bettr'] = df.at[names[i], 'bettr'] + 1
                if names[i] in raisetr:
                    df.at[names[i], 'raisetr'] = df.at[names[i], 'raisetr'] + 1
                    if ((len(raisetr) > 1) & (raisetr[-1] == names[i])):
                        df.at[names[i], 'reraisetr'] = df.at[names[i], 'reraisetr'] + 1
                    if ((len(raisetr) > 1) & (raisetr[-1] != names[i])):
                        df.at[names[i], 'numreraisedtr'] = df.at[names[i], 'numreraisedtr'] + 1
                    if ((len(raisetr) > 1) & (names[i] in foldtr)):
                        df.at[names[i], 'foldtoreraisetr'] = df.at[names[i], 'foldtoreraisetr'] + 1

            if rvstring:
                if names[i] in rvstring:
                    df.at[names[i], 'numplayedrv'] = df.at[names[i], 'numplayedrv'] + 1
                if names[i] in foldrv:
                    df.at[names[i], 'foldrv'] = df.at[names[i], 'foldrv'] + 1
                if raiserv:
                    if ((len(raiserv) >= 1) & (raiserv[-1] != names[i])):
                        df.at[names[i], 'numraisedrv'] = df.at[names[i], 'numraisedrv'] + 1
                    if ((len(raiserv) >= 1) & (names[i] in foldrv)):
                        df.at[names[i], 'foldtoraiserv'] = df.at[names[i], 'foldtoraiserv'] + 1
                if names[i] in callrv:
                    df.at[names[i], 'callrv'] = df.at[names[i], 'callrv'] + 1
                if names[i] in betrv:
                    df.at[names[i], 'betrv'] = df.at[names[i], 'betrv'] + 1
                if names[i] in raiserv:
                    df.at[names[i], 'raiserv'] = df.at[names[i], 'raiserv'] + 1
                    if ((len(raiserv) > 1) & (raiserv[-1] == names[i])):
                        df.at[names[i], 'reraiserv'] = df.at[names[i], 'reraiserv'] + 1
                    if ((len(raiserv) > 1) & (raiserv[-1] != names[i])):
                        df.at[names[i], 'numreraisedrv'] = df.at[names[i], 'numreraisedrv'] + 1
                    if ((len(raiserv) > 1) & (names[i] in foldrv)):
                        df.at[names[i], 'foldtoreraiserv'] = df.at[names[i], 'foldtoreraiserv'] + 1
                if (names[i] in seensd) & (len(seensd) > 1):
                    df.at[names[i], 'numplayedsd'] = df.at[names[i], 'numplayedsd'] + 1


time = 0.0
for filename in os.listdir('data'):
    start = timeit.default_timer()
    if filename.endswith('.txt'):
        print('reading:' + filename)
        extractstat('data/' + filename)
        stop = timeit.default_timer()
        print('Done reading', filename, 'in', round(stop - start, 2), 'sec.')
        time = round(time + stop - start, 2)
        print('Total elapsed:', time, 'sec.\n')
print('DONE!')

print(df)

df.at[df['numplayedpf'] == 0, 'numplayedpf'] = -1
df.at[df['numraisedpf'] == 0, 'numraisedpf'] = -1
df.at[df['numreraisedpf'] == 0, 'numreraisedpf'] = -1
df.at[df['numplayedfl'] == 0, 'numplayedfl'] = -1
df.at[df['numraisedfl'] == 0, 'numraisedfl'] = -1
df.at[df['numreraisedfl'] == 0, 'numreraisedfl'] = -1
df.at[df['numplayedtr'] == 0, 'numplayedtr'] = -1
df.at[df['numraisedtr'] == 0, 'numraisedtr'] = -1
df.at[df['numreraisedtr'] == 0, 'numreraisedtr'] = -1
df.at[df['numplayedrv'] == 0, 'numplayedrv'] = -1
df.at[df['numraisedrv'] == 0, 'numraisedrv'] = -1
df.at[df['numreraisedrv'] == 0, 'numreraisedrv'] = -1
df.at[df['numplayedsd'] == 0, 'numplayedsd'] = -1

df['bb/100hands'] = (df['net'] * 100)/df['numplayedpf']

df['avgstack'] = df['avgstack']/df['numplayedpf']
df['winpercent'] = df['winpercent']/df['numplayedpf']

df['foldpf'] = df['foldpf']/df['numplayedpf']
df['callpf'] = df['callpf']/df['numplayedpf']
df['raisepf'] = df['raisepf']/df['numplayedpf']
df['reraisepf'] = df['reraisepf']/df['numplayedpf']
df['foldtoraisepf'] = df['foldtoraisepf']/df['numraisedpf']
df['foldtoreraisepf'] = df['foldtoreraisepf']/df['numreraisedpf']

df['foldfl'] = df['foldfl']/df['numplayedfl']
df['callfl'] = df['callfl']/df['numplayedfl']
df['betfl'] = df['betfl']/df['numplayedfl']
df['raisefl'] = df['raisefl']/df['numplayedfl']
df['reraisefl'] = df['reraisefl']/df['numplayedfl']
df['foldtoraisefl'] = df['foldtoraisefl']/df['numraisedfl']
df['foldtoreraisefl'] = df['foldtoreraisefl']/df['numreraisedfl']
df['pctseenfl'] = df['numplayedfl']/df['numplayedpf']

df['foldtr'] = df['foldtr']/df['numplayedtr']
df['calltr'] = df['calltr']/df['numplayedtr']
df['bettr'] = df['bettr']/df['numplayedtr']
df['raisetr'] = df['raisetr']/df['numplayedtr']
df['reraisetr'] = df['reraisetr']/df['numplayedtr']
df['foldtoraisetr'] = df['foldtoraisetr']/df['numraisedtr']
df['foldtoreraisetr'] = df['foldtoreraisetr']/df['numreraisedtr']
df['pctseentr'] = df['numplayedtr']/df['numplayedpf']

df['foldrv'] = df['foldrv']/df['numplayedrv']
df['callrv'] = df['callrv']/df['numplayedrv']
df['betrv'] = df['betrv']/df['numplayedrv']
df['raiserv'] = df['raiserv']/df['numplayedrv']
df['reraiserv'] = df['reraiserv']/df['numplayedrv']
df['foldtoraiserv'] = df['foldtoraiserv']/df['numraisedrv']
df['foldtoreraiserv'] = df['foldtoreraiserv']/df['numreraisedrv']
df['pctseenrv'] = df['numplayedrv']/df['numplayedpf']

df['pctseensd'] = df['numplayedsd']/df['numplayedpf']

df.at[df['numplayedpf'] == -1, 'numplayedpf'] = 0
df.at[df['numraisedpf'] == -1, 'numraisedpf'] = 0
df.at[df['numreraisedpf'] == -1, 'numreraisedpf'] = 0
df.at[df['numplayedfl'] == -1, 'numplayedfl'] = 0
df.at[df['numraisedfl'] == -1, 'numraisedfl'] = 0
df.at[df['numreraisedfl'] == -1, 'numreraisedfl'] = 0
df.at[df['numplayedtr'] == -1, 'numplayedtr'] = 0
df.at[df['numraisedtr'] == -1, 'numraisedtr'] = 0
df.at[df['numreraisedtr'] == -1, 'numreraisedtr'] = 0
df.at[df['numplayedrv'] == -1, 'numplayedrv'] = 0
df.at[df['numraisedrv'] == -1, 'numraisedrv'] = 0
df.at[df['numreraisedrv'] == -1, 'numreraisedrv'] = 0
df.at[df['numplayedsd'] == -1, 'numplayedsd'] = 0

print(df)

df.to_csv('stats.csv')

