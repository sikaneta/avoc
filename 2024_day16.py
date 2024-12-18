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

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/16/input")

#%%
prod = resp.text[:-1].split('\n')

#%%
test1 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""[1:-1].split('\n')

test2 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""[1:-1].split('\n')

#%%
def propagate(mymap, mapcrds, q, r, thresh = 0):
    path = q.get()
    crd = path[-1]
    
    path_val = val(path)
    if mapcrds[crd[0]][crd[1]] is None:
        mapcrds[crd[0]][crd[1]] = path_val
    elif path_val > mapcrds[crd[0]][crd[1]] + thresh:
        return
    else:
        mapcrds[crd[0]][crd[1]] = path_val
    
    if mymap[crd[0]][crd[1]] == 'E':
        r.append(path)
    
    adjacent = [(0,-1),(-1,0),(1,0),(0,1)]
    
    new = [(crd[0]+shift[0], crd[1]+shift[1])
           for shift in adjacent 
           if mymap[crd[0]+shift[0]][crd[1]+shift[1]] !='#']
        
    for n in new:
        if n not in path:
            q.put(path + [n])
    
#%%
def val(path):
    prev_dir = (0,1)
    turns = 0
    for e1,e2 in zip(path[:-1], path[1:]):
        path_dir = (e2[0]-e1[0], e2[1]-e1[1])
        if path_dir != prev_dir:
            prev_dir = path_dir
            turns += 1
    return len(path)-1 + 1000*turns

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
mymap = [[x for x in row] for row in prod] 
M = len(mymap)
N = len(mymap[0])
maze_start = (None,None)
mapcrds = [[None]*N for k in range(M)]
for m,row in enumerate(mymap):
    for n,col in enumerate(row):
        if col == 'S':
            maze_start = (m,n)
            
pltMap(mymap)

q = queue.Queue()
r = list()
q.put([maze_start])

#%%
counter = 0
while not q.empty():
    propagate(mymap, mapcrds, q, r, thresh = 1000)
    counter += 1
    if counter % 1000000 == 1:
        print(q.qsize())
    

#%% Display a single path
[pltMap(mymap, p) for p in r[-2:]]

#%%
vals = [val(p) for p in r]
part1 = min(vals)
print("Part1: %d" % part1)

#%%
part2 = reduce(lambda x,y: x+y, [p for v,p in zip(vals, r) if v==part1])
print("Part2: %d" % len(set(part2)))
