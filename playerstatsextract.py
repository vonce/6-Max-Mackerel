import os

os.environ[
    'JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_161.jdk/Contents/Home"  # type which java in terminal and paste here
os.environ['CLASSPATH'] = "./Flounder.jar"
from jnius import autoclass
import re
import pandas as pd
import timeit

calculate = autoclass("flounder.Calculate")


def extractstat(txt):  # extracts text from Winning Poker Network datamined data.
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
        allnames = re.findall('Seat [\d]: (.*) \(', allgames[i])
        newnames = list(allnames)
        for j in range(len(allnames)):
            for char in ['_', '[', '\\', '^', '$', '.', '|', '?', '*', '+', '(', ')']:
                if char in allnames[j]:
                    newnames[j] = newnames[j].replace(char, '`')
        for j in range(len(allnames)):
            allgames[i] = allgames[i].replace(allnames[j], newnames[j])

    for game in allgames:

        '''
        stats = [
            name,
            avgstack,
            foldpf,
            callpf,
            raisepf,
            reraisepf,
            foldtoreraisepf,
            numplayedpf,
            foldfl,
            callfl,
            raisefl,
            reraisefl,
            foldtoreraisefl,
            numplayedfl,
            foldtr,
            calltr,
            raisetr,
            reraisetr,
            foldtoreraisetr,
            numplayedtr,
            foldrv,
            callrv,
            raiserv,
            reraiserv,
            foldtoreraiserv,
            numplayedrv,
        ]
        '''
    df = []
    statplayers = []


    df = pd.DataFrame(df)
    return df


alldata = []
time = 0.0
for filename in os.listdir('data'):
    start = timeit.default_timer()
    if filename.endswith('.txt'):
        print('reading:' + filename)
        alldata.append(extractstat('data/' + filename))
        stop = timeit.default_timer()
        print('Done reading', filename, 'in', round(stop - start, 2), 'sec.')
        time = round(time + stop - start, 2)
        print('Total elapsed:', time, 'sec.\n')
print('DONE!')

alldata = pd.concat(alldata)
alldata.to_csv('stats.csv')

