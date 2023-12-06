# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requests
from functools import reduce
import numpy as np

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/6/input")

#%%
lines = resp.text.split('\n')[:-1]

testlines = """
Time:      7  15   30
Distance:  9  40  200
""".split('\n')[1:-1]

#%% Test or the real thing
mylines = lines

#%% Functions
races = [{"time": int(t), "distance": int(d)} 
         for t,d in zip(mylines[0].split()[1:],
                        mylines[1].split()[1:])]

#%%
def distance(race):
    return [(race["time"] - m)*m -race["distance"] for m in range(race["time"])]

#%% Part 1
wins = map(lambda x: len([k for k in x if k> 0]), map(distance, races))
print("Part1: %d" % reduce(lambda x,y: x*y, wins))

#%% Part 2
N = int("".join(mylines[0].split()[1:]))
D = int("".join(mylines[1].split()[1:]))

W = np.sqrt((N/2)**2 - D)
if N %2 == 0:
    ways = 2*np.floor(W) + 1
else:
    ways = 2*np.ceil(W-0.5)
    
ways = print("Part2: %d" % ways)

