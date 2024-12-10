# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
from itertools import combinations
import numpy as np

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/10/input")

#%%
opmap = resp.text.split('\n')[:-1]

#%%
testmap = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""[1:-1].split('\n')

#%%
mymap = [[int(x) for x in t] for t in opmap]
MM = len(mymap)
NN = len(mymap[0])
#%%
def getVal(crds, mymap):
    row,col = crds
    return mymap[row][col] if (0 <= row < MM) and (0 <= col < NN) else -100
    
def navigate(crd, mymap):
    myVal = getVal(crd, mymap)
    if myVal == 9:
        return [tuple(crd)]
        
    row,col = crd
    NEWS = [[row, col+1],
            [row-1, col],
            [row+1, col],
            [row, col-1]]
    
    path = [getVal(pt, mymap) - myVal for pt in NEWS]
    return [x for y in [navigate(pt, mymap) 
                        for pt,p in zip(NEWS,path) if p == 1]
            for x in y]

#%%
total = []
for m, row in enumerate(mymap):
    for n, element in enumerate(row):
        if element == 0:
            total.append(len(set(navigate([m,n],mymap))))

#%%
part1 = sum(total)
print("Part 1: %d" % part1)

#%%
total = []
for m, row in enumerate(mymap):
    for n, element in enumerate(row):
        if element == 0:
            total.append(len(navigate([m,n],mymap)))

#%%
part2 = sum(total)
print("Part 2: %d" % part2)
