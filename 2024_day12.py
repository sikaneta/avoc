# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
from itertools import combinations, product
import numpy as np
from tqdm import tqdm

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/12/input")

#%%
inputmap = resp.text.split('\n')[:-1]

#%%
testmap = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".split('\n')[1:-1]

#%%
def metric(crd1, crd2):
    return abs(crd1[0] - crd2[0]) + abs(crd1[1] - crd2[1])

#%%
def similarity(mymap):
    M = len(mymap)
    N = len(mymap[0])
    crds = [(m,n) for m in range(M) for n in range(N)]
    nCrds = len(crds)
    sim = np.eye(nCrds)
    for m in tqdm(range(nCrds), desc="Computing similarity"):
        for n in range(m+1,nCrds):
            if mymap[crds[m][0]][crds[m][1]] == mymap[crds[n][0]][crds[n][1]]:
                score = metric(crds[m],crds[n])
                sim[m,n] = 0 if score > 1 else score 
    return sim + sim.T - np.eye(nCrds)

#%%
def sdot(v, sim):
    return np.sum([sim[k,:] for k,v in enumerate(v) if v == 1], axis=0)

#%%
def cluster(simMat):
    f = lambda x: min(x,1)
    vf = np.vectorize(f)
    m,n = simMat.shape
    clusterNumbers = np.arange(m)
    for row in tqdm(range(m), desc = "Clustering"):
        if row not in clusterNumbers:
            continue
        v = simMat[row,:]
        nv = np.zeros_like(v)
        while np.sum(v - nv) > 0:
            nv = v
            v = vf(sdot(v,simMat))
            #v = vf(nv.dot(simMat))
        clusterNumbers[np.argwhere(v==1)] = row    
            
    uniqueClst = sorted(list(set(list(clusterNumbers))))
    return np.array([uniqueClst.index(k) for k in clusterNumbers])

#%%
def neighbours(idx,sim):
    return sum([x for x in sim[idx,(idx+1):] if x==1])

def areaPerimeter(idxs, sim):
    area = len(idxs)
    return area, area*4 - sum(map(lambda x: neighbours(x,sim), idxs))*2

def filterPerimeter(idxs, crds, simMat):
    """ Get columns of cluster """
    mycrds = [crds[idx] for idx in idxs]
    cols = sorted(list(set([crds[idx][1] for idx in idxs])))
    rows = sorted(list(set([crds[idx][0] for idx in idxs])))
    
    col_vects = [[idx for idx in idxs if crds[idx][1] == col] for col in cols]
    row_vects = [[idx for idx in idxs if crds[idx][0] == row] for row in rows]
    
    col_vects = [[c for c in cols if sum(simMat[c,:]) < 5] 
                 for cols in col_vects]
    
    row_vects = [[r for r in rows if sum(simMat[:,r]) < 5] 
                 for rows in row_vects]

    total = 0
    for col1,col2 in zip(col_vects[:-1], col_vects[1:]):
        for c1,c2 in product(col1, col2):
            if crds[c1][0] != crds[c2][0]:
                continue
            if simMat[c1,c2] == 1:
                """ Check if an interior line """
                b = [(crds[x][0]-1, crds[x][1]) in mycrds for x in [c1,c2]]
                a = [(crds[x][0]+1, crds[x][1]) in mycrds for x in [c1,c2]]
                total += int(not any(a))
                total += int(not any(b))
    
    for row1,row2 in zip(row_vects[:-1], row_vects[1:]):
        for r1,r2 in product(row1, row2):
            if crds[r1][1] != crds[r2][1]:
                continue
            if simMat[r1,r2] == 1:
                b = [(crds[x][0], crds[x][1]-1) in mycrds for x in [r1,r2]]
                a = [(crds[x][0], crds[x][1]+1) in mycrds for x in [r1,r2]]
                total += int(not any(a))
                total += int(not any(b))
    
    return total
        
#%%      
mymap = inputmap
sim = similarity(mymap)    
M = len(mymap)
N = len(mymap[0])
crds = [(m,n) for m in range(M) for n in range(N)]
#%%       
clusters = cluster(sim)
u_clusters = set(clusters)

#%%
part1 = [areaPerimeter([idx for idx,cln in enumerate(clusters) if cln == c], sim) 
      for c in tqdm(u_clusters, desc="Area|Perimeter")]
#%%
print("Part1: %d" % sum([a*p for a,p in part1]))

#%%
allidxs = [[idx for idx,cln in enumerate(clusters) if cln == ucln] 
           for ucln in u_clusters]

#%%
pcorrect = [filterPerimeter(idxs, crds, sim) 
            for idxs in tqdm(allidxs, desc="Correcting perimeter")]

#%%
part2 = sum([int(p[0]*(p[1]-pc)) for p,pc in zip(part1,pcorrect)])
print("Part2: %d" % part2)
