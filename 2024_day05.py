# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
from itertools import combinations
import numpy as np

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/5/input")

#%%
rules, lines = resp.text.split('\n\n')
lines = lines[:-1]

#%%
rules, lines = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""[1:-1].split('\n\n')

#%%
rules = rules.split('\n')
lines = [l.split(',') for l in lines.split('\n')]

#%%
def checkline(line, rules):
    for x,y in combinations(line,2):
        if "%s|%s" % (y,x) in rules:
            return False
    return True

#%%
part1 = [int(line[int(len(line)/2)]) 
         for line in lines if checkline(line, rules)]

print("Part 1: %d" % sum(part1))

#%%
def reorder(line, rules):
    for x,y in combinations(range(len(line)),2):
        if "%s|%s" % (line[y],line[x]) in rules:
            """ Switch around """
            line[x],line[y] = line[y],line[x]
            if not checkline(line, rules):
                return reorder(line, rules)
    return line


#%%
part2 = [int(reorder(line, rules)[int(len(line)/2)]) 
         for line in lines if not checkline(line, rules)]
print("Part 2: %d" % sum(part2))
