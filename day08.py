# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requests
from functools import reduce
from egcd import egcd

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/8/input")

#%%
lines = resp.text.split('\n')[:-1]

testlines1 = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".split('\n')[1:-1]

testlines2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".split('\n')[1:-1]

testlines3 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".split('\n')[1:-1]

#%% Functions
def splitTokens(tline):
    yy = tline.split()
    return yy[0], (yy[-2][1:-1], yy[-1][:-1])

def parseLines(mylines):
    route = {x[0]:x[1] for x in map(splitTokens, mylines[2:])}
    route["instructions"] = [int(x) for x in mylines[0].replace('L','0')
                             .replace('R','1')]
    return route
        
#%%
mylines = testlines3

#%%
route = parseLines(mylines)
sequence = []
token = 'AAA'
N = len(route["instructions"])
index = 0
while token!='ZZZ':
    index = index % N 
    token = route[token][route["instructions"][index]]
    sequence.append(token)
    index += 1
#%%
print("Part1: %d" % len(sequence))

#%%
route = parseLines(lines)

#%%
def zseq(route, token):
    token_copy = []
    #isequence = []
    N = len(route["instructions"])
    index = 0
    while True:
        token_copy.append((token, index % N))
        token = route[token][route["instructions"][index % N]]
        #isequence.append(index)
        index += 1
        if (token, index % N) in token_copy:
            break
        
    #return token_copy, isequence, (token, index % N)
    return token_copy, (token, index % N)

#%%
mytokens = [t for t in route.keys() if t[-1]=='A']

#%%
def params(token):
    obs, itm = zseq(route, token)
    offset = obs.index(itm)
    cyclen = len(obs)-offset
    zidx = [k for k,foo in enumerate(obs) if foo[0][-1]=='Z']
    return offset, cyclen, zidx

#%%
blocks = list(map(params, mytokens))

#%%
egcd(blocks[0][1], blocks[1][1])
""" Have computed that 277 divides all cycle lengths """


#%%
rblen = [b[1]/277 for b in blocks]
""" These are all prime so relatively prime 
    To solve (m0+1)p0=(m1+1)p1=(m2+1)p2...
    set (m0+1)*p0 = p0*p1*p2*p3...
        (m1+1)*p1 = p0*p1*p2*p3...
    Since relatively prime, this is the solution """

steps1 = reduce(lambda x,y: x*y, rblen[1:])*blocks[0][1]
print("Part2: %d" % steps1)