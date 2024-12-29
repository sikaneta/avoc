# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""

#%%
import json
import requests
from tqdm import tqdm
from collections import defaultdict
import numpy as np
from itertools import product
import re

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/25/input")

#%%
prod = resp.text[:-1].split('\n\n')

#%%
test1 = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""[1:-1].split('\n\n')
    
#%% 
def parse(mydata):
    locks = []
    keys = []
    for item in mydata:
        rows = item.split('\n')
        if all(x=='#' for x in rows[0]):
            locks.append(np.array([[1 if x=='#' else 0 for x in row] 
                                  for row in rows[1:]]))
        else:
            keys.append(np.array([[1 if x=='#' else 0 for x in row] 
                                  for row in rows[:-1]]))
    return locks, keys
 
#%%
locks, keys = parse(prod)

#%%
lspace = [np.sum(lock, axis=0) for lock in locks]
kspace = [np.sum(key, axis=0) for key in keys]

combos = []
for l,k in product(lspace, kspace):
    if any(l+k > 5):
        pass
    else:
        combos.append((l,k))