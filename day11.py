# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requests
from itertools import product
from collections import defaultdict
from tqdm import tqdm

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/10/input")

#%%
lines = resp.text.split('\n')[:-1]

testlines = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""".split('\n')[1:-1]

testlines2 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""".split('\n')[1:-1]

testlines3 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".split('\n')[1:-1]

#%% Functions
def connections(mylines):
    rows = len(mylines)
    cols = len(mylines[0])
    # sim = np.eye(rows*cols, dtype=int)
    # crds = list(product(range(rows), range(cols)))
    conn = defaultdict(list)
    for c in product(range(rows), range(cols)):
        if mylines[c[0]][c[1]] in ['7','|','F'] and c[0] < rows - 1:
            conn["%d-%d" % c].append("%d-%d" % (c[0]+1, c[1]))
        if mylines[c[0]][c[1]] in ['L','|','J'] and c[0] > 0:
            conn["%d-%d" % c].append("%d-%d" % (c[0]-1, c[1]))
        if mylines[c[0]][c[1]] in ['L','-','F'] and c[1] < cols - 1:
            conn["%d-%d" % c].append("%d-%d" % (c[0], c[1]+1))
        if mylines[c[0]][c[1]] in ['7','-','J'] and c[1] > 0:
            conn["%d-%d" % c].append("%d-%d" % (c[0], c[1]-1))
        
    return conn

def follow(conn, x):
    neighbour = [n for n in conn[x[-1]] if n != x[0]]
    if len(neighbour) == 0:
        return x
    else:
        return [x[-1]] + neighbour

def touch(loop, links):
    idx = loop.index(links[0])
    left_links = []
    lidx = idx - 1
    while loop[lidx] in links:
        left_links.append(loop[lidx])
        lidx -= 1
    left_links.append(loop[lidx])
    
    ridx = idx + 1
    right_links = [links[0]]
    while loop[ridx] in links: 
        right_links.append(loop[ridx])
        ridx += 1
    right_links.append(loop[ridx])
    return left_links[-1::-1] + right_links
   
def crossing_num(loop, y):
    if y in loop:
        return -2
    row, col = y.split("-")
    def ray(l):
        rr, rc = l.split("-")
        return (rr==row) and (int(rc)>int(col))
    links = list(filter(ray, loop))
    
    score = 0
    while len(links) > 0:
        segment = touch(loop, links)
        links = [x for x in links if x not in segment[1:-1]]
        if segment[0].split("-")[0] != segment[-1].split("-")[0]:
            score += 1
    return score   

#%%
mylines = lines
srow = [row for row,rowdata in enumerate(mylines) if 'S' in rowdata][0]
scol = mylines[srow].index('S')
sc = "%d-%d" % (srow, scol)

conn = connections(mylines)
""" Next part done manually """
x = [sc, "%d-%d" % (srow+1, scol)]
trail = []
for k in range(len(mylines)*len(mylines[0])):
    x = follow(conn, x)
    if sc in x:
        break
    else:
        trail.append(x[-1])
    
loop = [sc, "%d-%d" % (srow+1, scol)] + trail + ["%d-%d" % (srow,scol)]

interior = []
for row in tqdm(range(len(mylines))):
    for col in range(len(mylines[0])):
        if crossing_num(loop, "%d-%d" % (row,col))%2 == 1:
            interior.append((row, col))
            
print("Part 2: %d" % len(interior))
 
