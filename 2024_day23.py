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
from itertools import combinations, takewhile
import re

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/23/input")

#%%
prod = resp.text[:-1].split('\n')

#%%
test1 = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""[1:-1].split('\n')
        
def addgroup(N, groups):
    M = len(groups[N])
    newgroup = []
    sortidxs = list(combinations(range(N), N-1))
    for sidx in tqdm(sortidxs, desc="(%d)" % M):
        cidx = [x for x in range(N) if x not in sidx][0]
        sarray = sorted(groups[N], key = lambda x: tuple([x[k] for k in sidx]))
        i = 0
        while i < M:
            stem = tuple(sarray[i][k] for k in sidx)
            subset = []
            while tuple(sarray[i][k] for k in sidx) == stem:
                subset.append(sarray[i][cidx])
                i += 1
                if i == M:
                    break
            for p in combinations(subset, 2):
                if p in groups[2]:
                    item = tuple(sorted(stem + p))
                    newgroup.append(item)
    groups[N+1] = sorted(list(set(newgroup)))
    
#%%
pairs = prod
options = list(set([x for y in [p.split('-') for p in pairs] for x in y]))
groups = defaultdict(list)
groups[2] = sorted([tuple(sorted([options.index(x[0:2]),options.index(x[3:5])])) 
                    for x in pairs])

#%%
N = 2
while len(groups[N]) > 0: 
    addgroup(N, groups)
    N = N + 1

#%%
triples = [",".join(sorted([options[kk] for kk in k])) for k in groups[3]]
biggest = [",".join(sorted([options[kk] for kk in k])) for k in groups[N-1]]
triples = [x for x in triples if re.search('t[a-z]', x) is not None]

print("Part1: %d" % len(triples))
print("Part2: %s" % biggest[0])