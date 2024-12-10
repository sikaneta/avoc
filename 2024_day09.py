# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
import numpy as np
from collections import defaultdict

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/9/input")

#%%
line,_ = resp.text.split('\n')

#%%
testline = """2333133121414131402"""

#%%
myline = testline
if len(myline)//2 != 0:
    myline = myline + '0'

files = [[[int(k/2)]*int(myline[k]),[None]*int(myline[k+1])]  
         for k in range(0,len(myline),2)]
    
    
#%%
rf_idxs = [x for y in files for x in y[0]][-1::-1]
n_fill = sum([len(x[1]) for x in files])

#%%
f_pos = 0
for file in files:
    e_pos = min(n_fill, f_pos + len(file[1]))
    file[1] = rf_idxs[f_pos:e_pos]
    f_pos = e_pos
    if f_pos >= n_fill:
        break

#%%
p_vals = [x for y in files for x in y[0]+y[1]][0:len(rf_idxs)]    
    
#%%
part1 = sum([k*p for k,p in enumerate(p_vals)])
print("Part 1: %d" % part1)

#%%
def part2process(files):
    high_pos = -1
    while high_pos > -len(files):# high in files[-1::-1]:
        high = files[high_pos]
        if not high:
            continue
        for low in files[:high_pos]:    
            if len(high[0]) <= len(low[1]):
                nlow = split([low[0] + high[0],
                              low[1][0:(len(low[1]) - len(high[0]))]])
                low_pos = files.index(low)
                files = files[0:low_pos] + nlow + files[(low_pos+1):]
                high[1] += [None]*len(high[0])
                high[0] = []
                break
        high_pos = high_pos - 1
        
    return files

#%%
def split(f):
    mydict =defaultdict(list)
    for k in f[0]:
        mydict[k].append(k)
    nf = [[val, []] for _,val in mydict.items()]
    try:
        nf[-1][-1] = f[1]
    except IndexError:
        nf = [f]
    return nf
        
#%%
myline = line
if len(myline)//2 != 0:
    myline = myline + '0'
files = [[[int(k/2)]*int(myline[k]),[None]*int(myline[k+1])]  
         for k in range(0,len(myline),2)]
files = part2process(files)
p2_vals = [x if x is not None else 0 for y in files for x in y[0]+y[1]] 
part2 = sum([k*p for k,p in enumerate(p2_vals)])
print("Part 2: %d" % part2)


