# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requests
from functools import reduce

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/2/input")

#%%
lines = resp.text.split('\n')[0:-1]

testlines = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".split('\n')[1:-1]

#%% 
def parseLine(line):
    game, scores = line.split(":")
    parsed = {"game": int(game.split()[-1]),
              "trials": []}
    trials = scores.split(";")
    for trial in trials:
        x = {"red": 0, "green": 0, "blue": 0}
        for y in [z.split() for z in trial.split(",")]:
            x[y[1]] = int(y[0])
        parsed["trials"].append(x)
    return parsed
 
def gamePass(x, mx_cols = {"red": 12, "green": 13, "blue": 14}):
    return all(max([t[color] for t in x["trials"]]) <= mx_cols[color] 
               for color in mx_cols.keys())

def gamePower(x):
    keys = "red green blue".split()
    return reduce(lambda x,y: x*y, 
                  [max([t[color] for t in x["trials"]]) 
                   for color in keys])

#%% Part 1
possible = filter(gamePass, map(parseLine, lines))
print("Part 1: %d" % sum([x["game"] for x in possible]))
    
#%% Part 2
power = sum(map(gamePower, map(parseLine, lines)))
print("Part 2: %d" % power)