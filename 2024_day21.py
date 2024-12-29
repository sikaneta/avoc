# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""

#%%
import json
import requests
import numpy as np
import queue
from collections import defaultdict

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/21/input")

#%%
prod = resp.text[:-1].split('\n')

#%%
test1 = """
029A
980A
179A
456A
379A
"""[1:-1].split('\n')

#%%
numeric = """
#####
#789#
#456#
#123#
##0A#
#####
"""[1:-1].split('\n')

directional = """
#####
##^A#
#<v>#
#####
"""[1:-1].split('\n')

arrows = {
    (-1,0): '^',
    (0,-1): '<',
    (0,1): '>',
    (1,0): 'v'}

edict = {
    "A": ["A"],
    "<A": ["v<<A", ">>^A"],
    ">A": ["vA", "^A"],
    "^A": ["<A",">A"],
    "vA": ["<vA", "^>A"],
    "<<A": ["v<<A", "A", ">>^A"],
    ">>A": ["vA","A","^A"],
    "^>A": ["<A", "v>A", "^A"],
    "<^A": ["v<<A", ">^A", ">A"],
    "<vA": ["v<<A", ">A", "^>A"],
    ">^A": ["vA", "<^A", ">A"],
    "v>A": ["<vA", ">A", "^A"],
    "v<A": ["<vA", "<A", ">>^A"],
    ">>^A": ["vA", "A", "<^A", ">A"],
    "v<<A": ["<vA", "<A", "A", ">>^A"]
    }

#%%
mycount = defaultdict(int)
def levelUp(code, N):
    if N>0:
        keys = [x for y in [levelUp(x, N-1) for x in edict[code]]
                for x in y]
        # for key in keys:
        #     mycount[key] += 1
        return keys
    else:
        return [code]
    
def tally(idict, N):
    odict = defaultdict(int)
    mykeys = list(idict.keys())
    for key in mykeys:
        for kkey in edict[key]:
            odict[kkey] += idict[key]

    if N == 0:
        return odict
    else:
        return tally(odict, N-1)
        

#%%   
def val(path):
    if len(path) < 2:
        return len(path)-1
    prev_dir = (path[1][0]-path[0][0],path[1][1]-path[0][1])
    turns = 0
    for e1,e2 in zip(path[:-1], path[1:]):
        path_dir = (e2[0]-e1[0], e2[1]-e1[1])
        if path_dir != prev_dir:
            prev_dir = path_dir
            turns += 1
    return len(path)-1 + 1000*turns

def propagate(mymap, mapcrds, q, r, target):
    path = q.get()
    crd = path[-1]
    
    path_val = val(path)
    if mapcrds[crd[0]][crd[1]] is None:
        mapcrds[crd[0]][crd[1]] = path_val
    elif path_val > mapcrds[crd[0]][crd[1]]:
        return
    else:
        mapcrds[crd[0]][crd[1]] = path_val
    
    if mymap[crd[0]][crd[1]] == target:
        r.append(path)
    
    adjacent = [(0,-1),(-1,0),(1,0),(0,1)]
    
    new = [(crd[0]+shift[0], crd[1]+shift[1])
           for shift in adjacent 
           if (mymap[crd[0]+shift[0]][crd[1]+shift[1]] !='#')]
        
    for n in new:
        if n not in path:
            q.put(path + [n])
    
def runMaze(mymap, maze_start, target):
    M = len(mymap)
    N = len(mymap[0])
    mapcrds = [[None]*N for k in range(M)]
    
    q = queue.Queue()
    r = list()
    q.put([maze_start])
    
    counter = 0
    while not q.empty():
        propagate(mymap, mapcrds, q, r, target)
        counter += 1
        
    if len(r) > 0:
        return r

def arrow_seq(crds):
    return [arrows[(x[0]-y[0], x[1]-y[1])] 
            for x,y in zip(crds[1:], crds[0:-1])]


def runSeq(seq, keypad, start_pos):
    full_path = []
    for k in seq:
        r = runMaze(keypad, start_pos, k)
        ridx = np.argmin([val(x) for x in r])
        full_path.append(r[ridx])
        start_pos = r[ridx][-1]
    return full_path

def getPart1Seq(code):
    lv = "".join(["".join(arrow_seq(x) + ['A']) 
                  for x in runSeq(code, numeric, (4,3))])
    
    for _ in ["1st robot", "2nd robot"]:
        lv = "".join(["".join(arrow_seq(x) + ['A']) 
                      for x in runSeq(lv, directional, (1,3))])

    return lv

def getPart2Seq(code, N):
    lv = "".join(["".join(arrow_seq(x) + ['A']) 
                  for x in runSeq(code, numeric, (4,3))])
    
    for _ in range(N):
        lv = "".join(["".join(arrow_seq(x) + ['A']) 
                      for x in runSeq(lv, directional, (1,3))])

    return lv

#%% Part 1
part1Codes = [(x,getPart1Seq(x)) for x in test1]
part1 = sum([int(x[0][:-1])*len(x[1]) for x in part1Codes])
print("Part1: %d" % part1)

#%%

nRobotDirKeypads = 25
p2N = nRobotDirKeypads - 1
part2 = list()
for ts in prod:
    toks = [x + 'A' 
            for x in getPart2Seq(ts, 1).split('A')[:-1]]
    tokdict = defaultdict(int)
    for t in toks:
        tokdict[t] += 1
    part2.append((int(ts[:-1]), 
                  sum([v for v in tally(tokdict, p2N).values()])))

print("Part2: %d" % sum([x[0]*x[1] for x in part2]))
