# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""

#%%
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
import queue
from functools import reduce
from collections import defaultdict
from tqdm import tqdm

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/20/input")

#%%
prod = resp.text[:-1].split('\n')

#%%
test1 = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""[1:-1].split('\n')


#%%
def propagate(mymap, mapcrds, q, r, cheat = (-10,-10)):
    path = q.get()
    crd = path[-1]
    
    path_val = val(path)
    if mapcrds[crd[0]][crd[1]] is None:
        mapcrds[crd[0]][crd[1]] = path_val
    # elif path_val > mapcrds[crd[0]][crd[1]] + thresh:
    #     return
    else:
        return
    
    if mymap[crd[0]][crd[1]] == 'E':
        r.append(path)
    
    adjacent = [(0,-1),(-1,0),(1,0),(0,1)]
    
    new = [(crd[0]+shift[0], crd[1]+shift[1])
           for shift in adjacent 
           if ((mymap[crd[0]+shift[0]][crd[1]+shift[1]] !='#')
               or ((crd[0]+shift[0], crd[1]+shift[1]) == cheat))]
        
    for n in new:
        if n not in path:
            q.put(path + [n])
    
#%%
def val(path):
    return len(path)-1

def pltMap(mymap, dd = []):
    cl = {'.': 0,
          '#': 1,
          'o': 5,
          'S': 3,
          'E': 3}
    data = np.zeros((len(mymap), len(mymap[0])))
    for m,row in enumerate(mymap):
        for n,el in enumerate(row):
            data[m,n] = cl[el]
            if (m,n) in dd:
                data[m,n] = 8
    plt.figure()
    plt.imshow(data)
    
#%%
def runMaze(mymap, maze_start, cheat = (-10,-10)):
    M = len(mymap)
    N = len(mymap[0])
    mapcrds = [[None]*N for k in range(M)]
    
    q = queue.Queue()
    r = list()
    q.put([maze_start])
    
    counter = 0
    while not q.empty():
        propagate(mymap, mapcrds, q, r, cheat = cheat)
        counter += 1
        
    if len(r) > 0:
        return r

def findCheats(mymap):
    lr = [(0,-1),(0,1)]
    ud = [(-1,0),(1,0)]
    vcheats = []
    hcheats = []
    ok = ['.', 'E', 'S']
    for m,row in enumerate(mymap):
        for n,col in enumerate(row):
            if col == '#':
                try:
                    lr_items = all([mymap[m+r][n+c] in ok for r,c in lr])
                    ud_items = all([mymap[m+r][n+c] in ok for r,c in ud])
                    if lr_items^ud_items:
                        if lr_items:
                            hcheats.append([(m,n-1), (m,n+1)])
                        else:
                            vcheats.append([(m-1,n), (m+1,n)])
                except IndexError:
                    pass
    return hcheats, vcheats

#%%
mymap = [[x for x in row] for row in prod] 
M = len(mymap)
N = len(mymap[0])
maze_start = (None,None)
mapcrds = [[None]*N for k in range(M)]
for m,row in enumerate(mymap):
    for n,col in enumerate(row):
        if col == 'S':
            maze_start = (m,n)
        if col == 'E':
            maze_end = (m,n)

#%%
r = runMaze(mymap, maze_start)
pltMap(mymap, r[0])
hcheats, vcheats = findCheats(mymap)
dd = [abs(r[0].index(y) - r[0].index(x))-2 for x,y in hcheats + vcheats]
h = defaultdict(int)
for k in dd:
    h[k] += 1

#%% Display a single path
part1 = sum([v for k,v in h.items() if k >= 100])
print("Part1: %d" % part1)

#%% Part 2
path = r[0]
pLen= len(path)

#%%
def boxLen(box):
    return (abs(box[0][0] - box[1][0])+ 
            abs(box[0][1] - box[1][1]))
    
#%%
tally = defaultdict(int)
for cN in tqdm(range(100,pLen), "finding shortcuts"):
    crds = [[path[k], path[k+cN+1]] for k,_ in enumerate(path) 
            if k + cN + 1 < pLen]
    bLen = [boxLen(x) for x in crds]
    bLen = [b for b in bLen if b <= 20]
    for bL in bLen:
        tally[cN - bL +1] += 1
        
#%%
print("Part2: %d" % sum([v for k,v in tally.items() if k>= 100]))