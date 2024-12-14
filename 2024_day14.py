# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
import numpy as np
import re
from collections import defaultdict
from functools import reduce
import matplotlib.pyplot as plt
from tqdm import tqdm

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/14/input")

#%%
inputrobots ={
"robots": resp.text[:-1].split('\n'),
"M": 103,
"N": 101
}


#%%
testrobots = {
"robots" : """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""[1:-1].split('\n'),
"M": 7,
"N": 11
}
#%%
def parserobot(robot):
    myre = "-*[0-9]+,-*[0-9]+"
    return [np.array([int(y) for y in x.split(",")]) 
             for x in re.findall(myre, robot)]

def propagate(robot, M, N, secs):
    new_pos = robot[0] + secs*robot[1]
    new_pos[0] = new_pos[0]%N
    new_pos[1] = new_pos[1]%M
    return [new_pos, robot[1]]

def countQuadrant(robots, M, N):
    n = (N//2)
    m = (M//2)
    quads = [[(0,n), (0,m)],
             [(n+1,N), (0,m)],
             [(0,n), (m+1,M)],
             [(n+1,N), (m+1,M)]]
    f = lambda x: np.array([int((y[0][0] <= x[0][0] < y[0][1]) and 
                                (y[1][0] <= x[0][1] < y[1][1])) 
                            for y in quads])
    result = np.sum(list(map(f,robots)), axis = 0)
    return result, reduce(lambda x,y: x*y, result)
             
def printRobots(robots, M, N):
    array = np.zeros((M,N))
    for robot in robots:
        array[robot[0][1], robot[0][0]] = 1
    plt.figure()
    plt.imshow(array)
    
def checkConnected(robots):
    items = [(x[0][0], x[0][1]) for x in robots]
    for item in items:
        test = [(item[0]+1, item[1]),
                (item[0]-1, item[1]),
                (item[0], item[1]+1),
                (item[1], item[1]-1),
                (item[0]-1, item[1]-1),
                (item[0]-1, item[1]+1),
                (item[0]+1, item[1]-1),
                (item[0]+1, item[1]+1)]
        for t in test:
            if t not in items:
                return False
    return True
        
#%%
myrobots = inputrobots
M = myrobots["M"]
N = myrobots["N"]
f = lambda rb: propagate(parserobot(rb), M, N, 3)
robots = list(map(f, myrobots["robots"]))
_, part1 = countQuadrant(robots, M, N)
print("Part1: %d" % part1)

#%%
robots = list(map(parserobot, myrobots["robots"]))
count = 1
#%%
symmetry = False
while not symmetry:
    robots = list(map(lambda x: propagate(x, M, N, 1), robots))
    count += 1
    quads, _ = countQuadrant(robots, M, N)
    if quads[0] == quads[1] and quads[2] == quads[3]:
        symmetry = True
print(count)
printRobots(robots, M, N)

#%%
robots = list(map(parserobot, myrobots["robots"]))
robots = list(map(lambda x: propagate(x, M, N, 1 + 73*103), robots))
count = 0
#%%
for k in range(20):
    robots = list(map(lambda x: propagate(x, M, N, 103), robots))
    count += 1
    printRobots(robots, M, N)

#%% By inspection
print("Part2: %d" % (1 + 73*103))
