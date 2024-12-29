# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""

#%%
import json
import requests
from tqdm import tqdm
import queue
from collections import defaultdict
import numpy as np

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/22/input")

#%%
prod = resp.text[:-1].split('\n')

#%%
def next(x):
    y = ((x << 6) ^ x) & 0xFFFFFF
    y = ((y >> 5) ^ y) & 0xFFFFFF
    y = ((y << 11) ^ y) & 0xFFFFFF
    
    return y

#%%
def genSecret(x, N):
    if N==0:
        return x
    else:
        return genSecret(next(x), N-1)
    
def difSecret(x, N):
    secrets = [None]*N
    secrets[0] = x
    for k in range(1,N):
        secrets[k] = next(secrets[k-1])
    return [x%10 for x in secrets]
    
def seqHist(seq):
    myhist = defaultdict(list)
    N = len(seq)
    for k in range(4,N):
        key = (seq[k-3] - seq[k-4],
               seq[k-2] - seq[k-3],
               seq[k-1] - seq[k-2],
               seq[k] - seq[k-1])
        myhist[key].append(seq[k])
    return myhist
        
#%%
part1 = [genSecret(int(x), 2000) for x in tqdm(prod)]
print("Part1: %d" % sum(part1))

#%%
myHist = defaultdict(list)
#for code in [1, 2, 3, 2024]:
for code in tqdm(prod):
    secrets = difSecret(int(code), 2000)
    sHist = seqHist(secrets)
    for k,v in sHist.items():
        myHist[k].append(v[0])

#%%
mKeys = list(myHist.keys())
mVals = [sum(v) for v in myHist.values()]
idx = np.argmax(mVals)
print("Part2: %d" % mVals[idx])