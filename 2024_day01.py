# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
from collections import Counter

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/1/input")

#%%
lines = resp.text.split('\n')[:-1]

testlines = """
3   4
4   3
2   5
1   3
3   9
3   3
""".split('\n')[1:-1]

#%%
rows = [[int(y)for y in x.split()] for x in lines ]
cols = tuple(zip(*rows))

#%%
part1 = sum([abs(x-y) for x,y in zip(*map(sorted, cols))])
print("Part 1: %d" % part1)

#%%
part2 = 0
cnt = Counter()
for k in cols[0]:
    if k not in cnt.keys():
        cnt[k] += sum([1 for x in cols[1] if x == k])
    part2 += k*cnt[k]
print("Part 2: %d" % part2)
