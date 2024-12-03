# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
from itertools import combinations

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/2/input")

#%%
lines = resp.text.split('\n')[:-1]

testlines = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".split('\n')[1:-1]

#%%
rows = [[int(y)for y in x.split()] for x in lines ]

#%%
f = lambda x: int((x[0]>=-3 and x[1]<=-1) or (x[0]>=1 and x[1]<=3))
def minmax_comp(row):
    derivative = [x-y for x,y in zip(row[0:-1],row[1:])]
    return f((min(derivative), max(derivative)))

#%%
part1 = map(minmax_comp, rows)
print("Part 1: %d" % sum(part1))

#%%
def skip(row):
    total = minmax_comp(row)
    for srow in combinations(row, len(row)-1):
        total += minmax_comp(srow)
    return min(1, total)

#%%
part2 = map(skip, rows)
print("Part 2: %d" % sum(part2))
