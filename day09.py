# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requestsreduce
from scipy.special import comb

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/9/input")

#%%
lines = resp.text.split('\n')[:-1]

testlines = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".split('\n')[1:-1]

#%% Functions
def level(N):
    return [int(comb(N,k))*(-1)**k for k in range(N+1)]

#%%
def applyLevel(series, N):
    return sum([x*y for x,y in zip(series[0:(N+1)], level(N))])

#%%
def decomposeLine(line):
    series = [int(x) for x in line.split()][-1::-1]
    Nelem = len(series)
    derivs = []
    for N in range(Nelem):
        deriv = applyLevel(series, N)
        if deriv == 0:
            break
        derivs.append(deriv)
    return derivs
        
#%%
mylines = lines
print("Part1: %d" % sum(map(lambda x: sum(decomposeLine(x)), mylines)))

#%%
def decomposeLineP2(line):
    series = [int(x) for x in line.split()]
    Nelem = len(series)
    derivs = []
    for N in range(Nelem - 1):
        deriv = sum([x*y for x,y in zip(series[0:(N+1)], level(N))])
        derivs.append(deriv)
    return derivs

#%% Part 2
print("Part1: %d" % sum(map(lambda x: sum(decomposeLineP2(x)), mylines)))
