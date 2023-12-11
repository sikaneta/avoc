# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requests
from itertools import combinations
from tqdm import tqdm

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/11/input")

#%%
lines = resp.text.split('\n')[:-1]

testlines = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".split('\n')[1:-1]

#%%
def between(interval, points):
    return sum([1 for x in points if interval[0]<x<interval[1] 
                or interval[1]<x<interval[0]])

def pairDistance(p1, p2, erows, ecols, expansion=1):
    dr = abs(p1[0] - p2[0]) + expansion*between((p1[0],p2[0]), erows)
    dc = abs(p1[1] - p2[1]) + expansion*between((p1[1],p2[1]), ecols)
    return dr + dc

#%%
mylines = lines

#%%
galaxies = []
rows = list(range(len(mylines)))
cols = list(range(len(mylines[0])))
for row, rdata in enumerate(mylines):
    for col, item in enumerate(rdata):
        if item != '.':
            galaxies.append([row,col])
            
#%%
grows = [g[0] for g in galaxies]
gcols = [g[1] for g in galaxies]
erows = [gr for gr in rows if gr not in grows]
ecols = [gc for gc in cols if gc not in gcols]

#%%
print("Part 1: %d" % sum([pairDistance(g1,g2,erows,ecols,expansion=1) 
                          for g1,g2 in tqdm(combinations(galaxies,2))]))

#%%
print("Part 2: %d" % sum([pairDistance(g1,g2,erows,ecols,expansion=999999) 
                          for g1,g2 in tqdm(combinations(galaxies,2))]))