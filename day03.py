# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requests

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/3/input")

#%%
lines = resp.text.split('\n')[0:-1]

testlines = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".split('\n')[1:-1]

#%% Test or the real thing
mylines = lines

#%% Functions

def clusterLine(line):
    tline = "".join(["%d-" % k if x.isdigit() else "." 
                     for k,x in enumerate(line)])
    tline.split(".")
    crds = [[int(x) for x in c.split("-") if len(x) > 0] for c in tline.split(".")]
    return [c for c in crds if len(c) > 0]

def clusterAttached(part, cluster, threshold=2.1):
    return any([(part[0]-cluster[0])**2 + (part[1]-c)**2 < threshold 
            for c in cluster[1]])

def partClusters(part, clusters):
    return part, [cluster for cluster in clusters
                  if clusterAttached(part,cluster)]
    
def cluster2num(cluster, mylines):
    return int(mylines[cluster[0]][min(cluster[1]):(max(cluster[1]) + 1)])
    

#%% Read parts and clusters
parts = [[(row,col,symb) for col,symb in enumerate(line) if not symb.isdigit()
          and symb != "."] 
         for row,line in enumerate(mylines)]
""" flatten """
parts = [x for y in parts for x in y]

clusters = [[(k,c) for c in clusterLine(line)] 
            for k,line in enumerate(mylines)]
""" flatten """
clusters = [c for y in clusters for c in y] 

#%% Part 1
""" Get clusters attached to a part """
a_clsts = [c for c in clusters 
           if any([clusterAttached(part,c) for part in parts])]

print("Part 1: %d" % sum([cluster2num(c, mylines) for c in a_clsts]))

    
#%% Part 2
""" filter parts for the gears only """
fltparts = filter(lambda x: x[-1]=="*", parts)

""" Get the clusters for the gear components """
myPartClusters = [partClusters(part, clusters) for part in fltparts]

""" Filter for exactly two attached clusters """
myPartClusters = filter(lambda x: len(x[1])==2, myPartClusters)

""" Retreive filtered cluster values """
nums = [[cluster2num(c,mylines) for c in pair] 
        for part, pair in myPartClusters]

print("Part 2: %d" % sum(map(lambda x: x[0]*x[1], nums)))
