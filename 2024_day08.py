# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
import numpy as np
from collections import defaultdict
from itertools import combinations

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/8/input")

#%%
lines = resp.text.split('\n')[0:-1]

#%%
testlines = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".split('\n')[1:-1]

#%%
antennas = defaultdict(list)
mymap = lines
for row, line in enumerate(mymap):
    for col, loc in enumerate(line):
        if loc != '.':
            antennas[loc].append(np.array([row,col]))
    
    
#%%
M = len(mymap)
N = len(mymap[0])

def valid(crd):
    return (0 <= crd[0] < M) and (0 <= crd[1] < N)
    
def antinodes(locations):
    found = []
    for a,b in combinations(locations, 2):
        l1 = 2*a - b
        l2 = 2*b - a
        found = found + [x for x in [l1,l2] if valid(x)]
    return ucrds(found)

def ucrds(crd_list):
    return [np.array(y) for y in set([tuple(x) for x in crd_list])]

#%%
part1_data = [antinodes(val) for key,val in antennas.items()]
part1 = len(ucrds([x for y in part1_data for x in y]))
print("Part 1: %d" % part1)

#%%
def antinodes2(locations):
    locs = [np.array(y) for y in sorted([tuple(x) for x in locations])]
    found = []
    for a,b in combinations(locs, 2):
        delta = b-a
        
        left = []
        k = 0
        while(valid(a - k*delta)):
            left.append(a - k*delta)
            k += 1
            
        right = []
        kk = 0
        while(valid(b + kk*delta)):
            right.append(b + kk*delta)
            kk += 1
            
        found = found + left + right
    return ucrds(found)

#%%
part2_data = [antinodes2(val) for key,val in antennas.items()]
part2 = len(ucrds([x for y in part2_data for x in y]))
print("Part 2: %d" % part2)


