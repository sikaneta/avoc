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
resp = session.get("https://adventofcode.com/2024/day/18/input")

#%%
prod = resp.text[:-1].split('\n')

#%%
test1 = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""[1:-1].split('\n')

#%%
def makemaze(xcrds, Nbytes, N):
    mymap = [['#']*(N+2)]
    mymap += [['#'] + ['.']*N + ['#'] for k in range(N)]
    mymap += [['#']*(N+2)]
    for crd in xcrds[:Nbytes]:
        mymap[crd[1]][crd[0]] = '#'
    mymap[1][1] = 'S'
    mymap[N][N] = 'E'
    return mymap

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
        return
        #mapcrds[crd[0]][crd[1]] = path_val
    
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
def runBytes(xcrds, idx, mazeN):
    mymap = makemaze(xcrds, idx, mazeN)
    M = len(mymap)
    N = len(mymap[0])
    mapcrds = [[None]*N for k in range(M)]
    maze_start = (1,1)
    
    q = queue.Queue()
    r = list()
    q.put([maze_start])
    
    counter = 0
    while not q.empty():
        propagate(mymap, mapcrds, q, r, thresh = 0)
        counter += 1
        #if counter % 10000 == 1:
            #print(q.qsize())
        
    if len(r) > 0:
        pltMap(mymap, r[-1])
        return r

#%%
xcrds = [tuple([int(y)+1 for y in x.split(",")]) for x in prod] 

#%% Display a single path
runBytes(xcrds, 3000, 71)

""" This part done manually until we find the idx in runBytes that causes
    the path to fail. A simple manual binary search works fine. """
