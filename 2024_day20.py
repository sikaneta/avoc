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
resp = session.get("https://adventofcode.com/2024/day/19/input")

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

#%%
mymap = [[x for x in row] for row in test1] 
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
pltMap(mymap)
r = runMaze(mymap, maze_start, cheat = (1,8))
pltMap(mymap, r[0])

#%% Display a single path
runBytes(xcrds, 3000, 71)

""" This part done manually until we find the idx in runBytes that causes
    the path to fail. A simple manual binary search works fine. """
