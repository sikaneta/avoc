# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
from tqdm import tqdm

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/7/input")

#%%
lines = resp.text.split('\n')[0:-1]

#%%
testlines = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".split('\n')[1:-1]

#%%
def add(x,y):
    return x + y
def mul(x,y):
    return x * y
def cat(x,y):
    return int("%d%d" % (x,y))

def chomp(target, val, array, operators = [add, mul]):
    if val > target or len(array) ==0:
        return False
    
    candidates = [f(val,array[0]) for f in operators]
    
    if any([x==target and len(array)==1 for x in candidates]):
        return True
    else:
        return any([chomp(target, c, array[1:], operators = operators) 
                    for c in candidates]) 
    return False
    
    
#%%
def parse(operation):
    val, elements = operation.split(': ')
    val = int(val)
    elements = [int(x) for x in elements.split(" ")]
    return val, elements


#%%
operations = lines
part1 = 0
for operation in tqdm(operations):
    val, elements = parse(operation)
    if chomp(val, elements[0], elements[1:]):
        part1 += val

print("Part 1: %d" % part1)

#%%
operations = lines
part2 = 0
for operation in tqdm(operations):
    val, elements = parse(operation)
    if chomp(val, elements[0], elements[1:], [add,mul,cat]):
        part2 += val

print("Part 2: %d" % part2)


