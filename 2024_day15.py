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
resp = session.get("https://adventofcode.com/2024/day/15/input")

#%%
prod = resp.text[:-1]

#%%
test1 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""[1:-1]

#%%
test2 = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""[1:-1]

#%%
class element:
    def __init__(self, row, col, etype):
        self.row = row
        self.col = col
        self.etype = etype
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def score(self):
        return 100*self.row + self.col
    
#%%
def propagate(mapcrds, el, shift):
    new = element(el.row+shift[0], el.col+shift[1], el.etype)
    if new in mapcrds['#']:
        return False
    else:
        idx = mapcrds[el.etype].index(el)
        if new not in mapcrds['O']:
            mapcrds[el.etype][idx] = new
            return True
        else:
            toshift = mapcrds['O'][mapcrds['O'].index(new)]
            if propagate(mapcrds, toshift, shift):
                mapcrds[el.etype][idx] = new
                return True
            
                
    return False
    
#%%
def printMap(mapcrds, M, N):
    toprint = [['.']*N for _ in range(M)]
    for el in mapcrds['@'] + mapcrds['O'] + mapcrds['#']:
        toprint[el.row][el.col] = el.etype
    print("\n".join(["".join(x) for x in toprint]))
#%%
mapdata, moves = prod.split('\n\n')
mymap = mapdata.split('\n')
moves = moves.replace('\n', '')
M = len(mymap)
N = len(mymap[0])
mapcrds = defaultdict(list)
for m,row in enumerate(mymap):
    for n,col in enumerate(row):
        mapcrds[col].append(element(m,n,col))

directions = {'<': (0,-1),
              '^': (-1,0),
              'v': (1,0),
              '>': (0,1)}

for c in tqdm(moves, desc='Making moves'):
    res = propagate(mapcrds, mapcrds['@'][0], directions[c])
    
part1 = sum([x.score() for x in mapcrds['O']])
print("")
print("Part1: %d" % part1)

#%%
typmap = {'#': '##',
          'O': '[]',
          '@': '@.',
          '.': '..'}
class ele:
    def __init__(self, row, col1, col2, etype):
        self.row = row
        if etype != '@':
            self.col = [col1, col2]
        else:
            self.col = [col1]
        self.etype = etype
    
    def __eq__(self, other):
        return (self.row == other.row) and any([x in self.col 
                                                for x in other.col])
    
    def score(self):
        return 100*self.row + self.col[0]
    
    def adjacent(self, other):
        union = self.col + other.col
        span = list(range(min(union), max(union)+1))
        gap = len([x for x in span if x not in union])
        if self.row == other.row and gap==0:
            return True
        if abs(self.row - other.row) == 1 and gap==0:
            return True
        return False
    
#%%
def prop(mapcrds, el, shift, action="act"):
    if el.etype == '@':
        col1 = 0
    else:
        col1 = el.col[1]
    new = ele(el.row+shift[0], 
              el.col[0]+shift[1], 
              col1+shift[1],
              el.etype[0])
    newnew = ele(el.row+shift[0], 
                 el.col[0]+2*shift[1], 
                 col1+2*shift[1],
                 el.etype[0])
    if new in mapcrds['#']:
        return False
    else:
        idx = mapcrds[el.etype].index(el)
        if (new not in mapcrds['O']) or (newnew not in mapcrds['O']):
            if action == "act":
                mapcrds[el.etype][idx] = new
            return True
        else:
            idx1 = mapcrds['O'].index(new)
            idx2 = mapcrds['O'].index(newnew)
            if not mapcrds['O'][idx1].adjacent(mapcrds['O'][idx2]):
                if action == "act":
                    mapcrds[el.etype][idx] = new
                return True
            tshift_arr = [x for x in mapcrds['O'] if x==newnew]
            #toshift = mapcrds['O'][mapcrds['O'].index(newnew)]
            if all([prop(mapcrds, toshift, shift, action=action) 
                    for toshift in tshift_arr]):
                if action == "act":
                    mapcrds[el.etype][idx] = new
                return True
            
                
    return False

def pMap(mapcrds, M, N):
    toprint = [['.']*(2*N) for _ in range(M)]
    for el in mapcrds['@'] + mapcrds['O'] + mapcrds['#']:
        toprint[el.row][el.col[0]] = typmap[el.etype][0]
        if el.etype != '@':
            toprint[el.row][el.col[1]] = typmap[el.etype][1]
    print("\n".join(["".join(x) for x in toprint]))

#%%
mapdata, moves = prod.split('\n\n')
mymap = mapdata.split('\n')
moves = moves.replace('\n', '')
M = len(mymap)
N = len(mymap[0])
mapcrds = defaultdict(list)
for m,row in enumerate(mymap):
    for n,col in enumerate(row):
        mapcrds[col].append(ele(m,2*n,2*n+1,col))

#%%
for c in tqdm(moves, desc='Making moves'):
    res = prop(mapcrds, mapcrds['@'][0], directions[c], action="assess")
    if res:
        prop(mapcrds, mapcrds['@'][0], directions[c])
    #print(c)
print('\n')
pMap(mapcrds, M, N)

part2 = sum([x.score() for x in mapcrds['O']])
print("Part1: %d" % part2)