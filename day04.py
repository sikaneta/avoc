# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requests
from tqdm import tqdm

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/4/input")

#%%
lines = resp.text.split('\n')[0:-1]

testlines = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".split('\n')[1:-1]

#%% Test or the real thing
mylines = lines

#%% Functions

def parseLine(line):
    card, scores = line.split(":")
    winner, played = scores.split("|")
    return{"card": card.split()[-1],
           "winners": [int(x) for x in winner.split()],
           "played": [int(x) for x in played.split()]}

def points(card):
    points = [2 for x in card["played"] if x in card["winners"]]
    return 2**(len(points)-1) if len(points)>0 else 0

def winners(card):
    return len([1 for x in card["played"] if x in card["winners"]])
        
#%%
print("Part 1: %d" % sum(map(lambda x: points(parseLine(x)), mylines)))

#%%
cards = list(map(parseLine, mylines))

#%%
def cardScore(k):
    N = winners(cards[k])
    return 1 + sum([cardScore(k+l+1) for l in range(N)])

#%% Very slow
print("Part 2: %d" % sum([cardScore(k) for k in tqdm(range(len(cards)))]))

    
