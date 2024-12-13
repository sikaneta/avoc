# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
from itertools import combinations
from collections import defaultdict
from tqdm import tqdm

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/11/input")

#%%
inputseed,_ = resp.text.split('\n')

#%%
testseed = """125 17"""

#%%
def f(num):
    if num == 0:
        return [1]
    num_str = "%d" % num
    num_len = len(num_str)
    if num_len%2 == 1:
        return [num*2024]
    else:
        return [int(num_str[:(num_len//2)]),
                int(num_str[(num_len//2):])]
    
#%%
seed = [int(x) for x in inputseed.split()]
for k in range(25):
    seed = [x for y in map(f,seed) for x in y]

print("Part1: %d" % len(seed))
    
#%% New fast method for part 2
def procnum(hist):
    new_hist = defaultdict(int)
    for key,val in hist.items():
        seed = f(key)
        for item in seed:
            new_hist[item] += val
    return new_hist

#%%
seed = [int(x) for x in testseed.split()]
hist = defaultdict(int)
for val in seed:
    hist[val] += 1
    
for k in tqdm(range(75)):
    hist = procnum(hist)

part2 = sum([val for _,val in hist.items()])
print("Part2: %d" % part2)

