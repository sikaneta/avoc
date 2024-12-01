# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requests
from itertools import combinations
from tqdm import tqdm
from math import comb
from collections import defaultdict
from functools import reduce
from math import factorial

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/12/input")

lines = resp.text.split('\n')[:-1]

#%%
testlines = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""".split('\n')[1:-1]

#%%
mylines = lines

#%%
def parseLine(myline):
    data, groups = myline.split()
    chunks = [x for x in data.split('.') if x]
    return data + ".", chunks, [int(x) for x in groups.split(",")]


def parseLineP2(myline,reps=5):
    data, groups = myline.split()
    data = "?".join([data]*reps)
    chunks = [x for x in data.split('.') if x]
    return data + ".", chunks, [int(x) for x in groups.split(",")]*reps

#%%
def valid(data, k, N):
    try:
        return (all(data[k+i] in ["#","?"] for i in range(N)) 
                and data[k+N] in [".","?"])
    except IndexError:
        return False
    
#%%
# def chomp(chunk, groups):
#     Nd = len(chunk)
#     Ng = len(groups)
#     cdict = []
#     kg = 0
#     while sum(groups[:(kg+1)]) <= Nd and kg < Ng:
#         N = path(chunk+'.', 0, groups[:(kg+1)])
#         if N != 0:
#             cdict.append((N, groups[(kg+1):]))
#         kg += 1
#     return cdict

#%%
def appetite(chunk, groups):
    Nc = len(chunk)
    mychunk = chunk + "."
    #npath = []
    grps = []
    for k in range(len(groups)):
        if sum(groups[:k]) > Nc:
            break
        gr = path(mychunk, 0, groups[:(k+1)])
        if gr > 0:
            grps.append((gr, groups[:(k+1)]))
        #npath.append(gr)
        
    mychunk = chunk + "?"
    bang = [k for k in range(len(chunk)) if mychunk[k:(k+2)]=="#?"]
    gidx = 0
    if len(bang) != 0:
        while len(bang) > 0 and gidx < len(groups):
            idx = bang[0] + groups[gidx] + 1
            bang = [x for x in bang if x >= idx]
            gidx += 1
    must = [x for x in grps if x[1]==groups[:gidx]]
    can = [x for x in grps if x[1]!=groups[:gidx]]
    # for k in range(gidx, len(npath)):
    #     if npath[k] !=0:
    #         can.append(groups[:(k+1)])
    return must, can

#%% Working fiel
def combinatoricpath(chunk, groups):
    # Find the indexes of each '#'
    # bang = [k for k,x in enumerate(chunk) if x=='#']
    
    try:
        bidx = chunk.index('#')
    except ValueError:
        return pigiegies(len(chunk) - sum(groups) - len(groups) + 1, 
                         len(groups)+1)[-1]
        
    #Nd = len(chunk)
    #Ng = len(groups)
    k = 1
    while sum(groups[:k]) < bidx:
        sNg = sum(groups[:k])
        N = len(chunk) - sNg - k + 1
        pidx = bidx - sNg
        psum = 0 if pidx < 0 else pigiegies(N,k+1)[pidx]
        if psum > 0:
            return psum*combinatoricpath(chunk[(bidx+1):], groups[k:])
 
#%%
    # for blen in bang:
    #     mychunk = "?"*len(chunk)
    #     mychunk[bang]
    #     pigiegies(len(chunks[0])-sum(groups)-len(groups)+1,len(groups)+1)

def process(chunks, groups):
    # print(chunks)
    # print(groups)
    if len(chunks)==0 and len(groups) > 0:
        return 0
    if len(chunks)==0 and len(groups) == 0:
        return 1
    if len(groups) == 0 and len(chunks) > 0:
        if any('#' in x for x in chunks):
            return 0
        return 1
    
    total = 0
    must, can = appetite(chunks[0], groups)
    if len(must)==0:# and len(can)==0:
        total += process(chunks[1:],groups)
    
    for x in must + can:
        head = x[0]#path(chunks[0] + '.', 0, x)
        tail = process(chunks[1:], groups[len(x[1]):])
        total += head*tail
        
    return total
    

#%%        
    
            
        
    
    
    
    
# def eat(chunk, groups):
#     Nd = len(chunk)
#     Ng = len(groups)
#     bang = [k for k,x in enumerate(chunk) if x=="#"]
    
#     cdict = []
#     kg = 0
#     while sum(groups[:(kg+1)]) <= Nd and kg < Ng:
#         N = path(chunk+'.', 0, groups[:(kg+1)])
#         if N != 0:
#             cdict.append((N, groups[(kg+1):]))
#         kg += 1
#     return cdict

# def process(mychunks, groups):
#     total = 0
#     # if len(chunks) == 0:
#     #     return 1
#     if len(mychunks)==0 and len(groups) > 0:
#         return 0
#     split = chomp(mychunks[0], groups)
#     if len(split) == 0:
#         if len(mychunks) > 0:
#             return process(mychunks[1:], groups)
#         else:
#             return 0
#     for x in split:
#         if len(x[1]) > 0:
#             # rest = sum([process(mychunks[k:], x[1]) 
#             #             for k in range(1,len(mychunks))])
#             # total += x[0]*rest
#             total += x[0]*process(mychunks[1:], x[1])
#         else:
#             total += x[0]
#     return total
        
        # M = sum(groups[:(kg+1)])
        # if Ng-1>M:
        #     break
        # for k in range(Ng-1,M):
        #     cdict[kg] += path(chunk+'.', 0, groups[:(kg+1)])
    # for kg,g in enumerate(groups):
    #     M = sum(groups[:(kg+1)])
    #     if Ng-1>M:
    #         break
    #     for k in range(Ng-1,M):
    #         cdict[kg] += path(chunk+'.', 0, groups[:(kg+1)])
                
        
        

def path(data, k, groups):
    
    if len(groups) == 0:
        l = min(k,len(data)-1)
        if "#" in data[l:]:
            return 0
        else:
            return 1
        
    if k>=len(data):
        return 0
    
    """ Case . """
    if data[k] == ".":
        return path(data, k+1, groups)
    
    """ Case # or ? """
    if not (valid(data,k,groups[0])):
        if data[k] == "#":
            return 0
        else:
            return path(data, k+1, groups)
    
    if data[k] == "#":
        return path(data, k+groups[0]+1, groups[1:])
    
    return path(data, k+groups[0]+1, groups[1:]) + path(data, k+1, groups)

def rep(line, reps):
    data, groups = parseLineP2(line, reps=reps)
    return path(data, 0, groups)

#%%
def ck(k,l):
    return reduce(lambda x,y: x*y, range(l+1,k+1))

def pigiegies(N,M):
    """
    Number of ways to put N identical pigeons into M holes
    
    Each hole represents a home for a pigeon. Pigeons can share holes. If
    N>M, then at least one hole contains more than one pigeon - the famous
    pigeon hole principle.

    Parameters
    ----------
    N : int
        Number of pigeons.
    M : int
        Number of holes/nests.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    f=[1, M]
    for k in range(1,N):
        f.append(sum([(M*f[l]*(k-l+1) - f[l+1])*ck(k,l) 
         for l in range(k)] + [M*f[-1]]))
        
    return [int(x/factorial(k)) for k, x in enumerate(f)]

#%%
mylines = lines
pool = list(map(parseLine, mylines))
routes = [path(p[0], 0, p[2]) for p in pool]

print("Part1: %d" % sum(routes))

#%%
pool2 = list(map(lambda x: parseLineP2(x, reps=2), mylines))
routes2 = [process(p[1], p[2]) for p in tqdm(pool2)]

#%%
pool3 = list(map(lambda x: parseLineP2(x, reps=3), mylines))
routes3 = []
for k in range(len(pool3)):
    p = pool3[k]
    print(k)
    if len(p[1]) > 1:
        routes3.append(process(p[1], p[2]))
    else:
        routes3.append(path(p[0], 0, p[2]))

#%%
pool5 = list(map(lambda x: parseLineP2(x, reps=5), mylines))
routes5 = []
for k in range(len(pool5)):
    p = pool5[k]
    print(k)
    if routes2[k]/routes[k] == routes3[k]/routes2[k]:
        routes5.append(routes[k]*(routes2[k]/routes[k])**4)
    if len(p[1]) > 1:
        routes5.append(process(p[1], p[2]))
    else:
        routes5.append(path(p[0], 0, p[2]))
    
#routes2 = [process(p[1], p[2]) for p in tqdm(pool)]


#%%
print("Part2: %d" % sum(routes2))