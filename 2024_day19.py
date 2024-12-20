# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
from tqdm import tqdm
from itertools import product
from collections import defaultdict

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/19/input")

#%%
prod = resp.text[:-1].split('\n\n')

#%%
test1 = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""[1:-1].split('\n\n')

#%%
def sim(tok, solns, word):
    N = len(word)
    rdict = defaultdict(int)
    for t1,t2 in product(tok.keys(), solns.keys()):
        ss = t1+t2
        Nss = len(ss)
        if Nss > N:
            continue
        if ss in word:
            rdict[ss]+= solns[t2]
    return rdict

def testword(tokens, word):
    ntok = defaultdict(int)
    for x in set([t for t in tokens if t in word]):
        ntok[x] += 1
    nntok = sim(ntok, ntok, word)
    solns = nntok[word]
    while len(nntok)>0:
        nntok = sim(ntok, nntok, word)
        if word in nntok.keys():
            solns += nntok[word]
    return solns

#%%
trial = prod
tokens = set(trial[0].split(', '))
words = trial[1].split('\n')

#%%
part12 = [testword(tokens, word) for word in tqdm(words)]

#%%
print("Part1: %d" % sum([1 for x in part12 if x != 0]))
print("Part2: %d" % sum(part12))
