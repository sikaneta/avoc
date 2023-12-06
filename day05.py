# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requests
from collections import defaultdict
from functools import reduce

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/5/input")

#%%

lines = (resp.text + '\n').split('\n\n')

testlines = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

""".split('\n\n')[:-1]

#%% Test or the real thing
mylines = lines

#%% Functions
def mapnum(k, maplines):
    tokens = maplines.split('\n')
    for token in tokens[1:]:
        rng = [int(k) for k in token.split()]
        if rng[1] <= k < rng[1] + rng[-1]:
            return k + rng[0] - rng[1]
    return k
    
def intersection(r1, r2):
    if r1[-1] <= r2[0] or r2[-1] <= r1[0]:
        return []
    return [k for k in sorted(list(r1) + list(r2))[1:3]]

def difference(r1, r2):
    r1andr2 = intersection(r1, r2)
    if len(r1andr2) == 0:
        return [r1]
    retval = []
    if r1andr2[0] > r1[0]:
        retval.append([r1[0], r1andr2[0]])
    if r1andr2[1] < r1[1]:
        retval.append([r1andr2[1], r1[1]])
    return retval

def joinmap(map1, map2):
    tokens1 = [int(x) for x in map1.split()]
    tokens2 = [int(x) for x in map2.split()]
    t1andt2 = intersection([tokens1[0], tokens1[0]+tokens1[-1]],
                           [tokens2[1], tokens2[1]+tokens2[-1]])
    t1minust2 = difference([tokens1[0], tokens1[0]+tokens1[-1]],
                           [tokens2[1], tokens2[1]+tokens2[-1]])
    t2minust1 = difference([tokens2[1], tokens2[1]+tokens2[-1]],
                           [tokens1[0], tokens1[0]+tokens1[-1]])
    t1d = tokens1[1] - tokens1[0]
    t2d = tokens2[1] - tokens2[0]
    m1 = [i + t1d for i in t1andt2]
    joined = defaultdict(list)
    if len(m1) > 0:
        joined["intersection"] = ["%d %d %d" % (t1andt2[0] - t2d, 
                       m1[0], m1[1]-m1[0])]
    for pair in t1minust2:
        joined["primary"].append("%d %d %d" % (pair[0], pair[0] + t1d, pair[1]-pair[0]))
    for pair in t2minust1:
        joined["secondary"].append("%d %d %d" % (pair[0] - t2d, pair[0], pair[1]-pair[0]))
        
    return joined

def coupleMapRec(primary, secondary):
    for pk in range(len(primary)):
        for sk in range(len(secondary)):
            group = joinmap(primary[pk], secondary[sk])
            if "intersection" in group.keys():
                newp = primary[:pk] + group["primary"] + primary[(pk+1):]
                news = secondary[:sk] + group["secondary"] + secondary[(sk+1):]
                return group["intersection"] + coupleMapRec(newp, news)
    
    return primary + secondary

def breadCrumbs(seed, dcts):
    for dct in dcts:
        seed = mapnum(seed, dct)
    return seed
        
def iIntersect(v1, v2):
    s = sorted(list(v1) + list(v2))
    if (s[1]==v1[1] and s[2]==v2[0]) or (s[1]==v2[1] and s[2]==v1[0]):
        return None
    else:
        return s[1:3]
    
#%%
seeds = [int(k) for k in mylines[0].split(':')[-1].split('\n')[0].split()]

print("Part 1: %d" % min(map(lambda x: breadCrumbs(x,mylines[1:]), seeds)))

#%%
seedlist = [int(x) for x in mylines[0].split(":")[-1].split()]
sline = [(seedlist[k], seedlist[k] + seedlist[k+1]) 
 for k in range(0,len(seedlist),2)]
mymaps = [l.split('\n')[1:] for l in mylines[1:]]
jj = reduce(coupleMapRec, mymaps)
jjstr = ["combinedline:\n" + "\n".join(jj)]
print("testing combined line: %d" % breadCrumbs(79, jjstr))
jjnum = [[int(x) for x in y.split()] for y in jj]
jjset = [(y[1], y[1]+y[2]) for y in jjnum]

iset = [(iIntersect(x,y),mp) for x in sline for y,mp in zip(jjset, jjnum)]
iset = [x for x in iset if x[0] is not None] 
bounds = lambda x: (x[0][0] - x[1][1] + x[1][0], x[0][1] - x[1][1] + x[1][0])
print("Part 2: %d" % min(min(map(bounds, iset), key = lambda x: min(x))))

    
