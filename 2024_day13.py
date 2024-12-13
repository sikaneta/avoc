# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
import numpy as np
import re

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/13/input")

#%%
inputmachines = resp.text[:-1].split('\n\n')

#%%
testmachines = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""[1:].split('\n\n')

#%%
def parsemachine(mach, offset=0):
    nums = [int(x[1:]) for x in re.findall("[+=][0-9]*", mach)]
    return (np.array([[nums[0],nums[2]],[nums[1],nums[3]]], dtype=np.int64), 
            np.array([[nums[4]+offset],[nums[5]+offset]], dtype=np.int64))

def invert(M):
    det = M[0,0]*M[1,1] - M[0,1]*M[1,0]
    Minv = np.array([[M[1,1], -M[0,1]],[-M[1,0], M[0,0]]], dtype=np.int64)
    return Minv, det

def trymachine(mach, offset=0):
    M,b = parsemachine(mach, offset)
    Minv, det = invert(M)
    return [x//det if x%det==0 else False for x in Minv.dot(b)[:,0]]
    
#%% Part 1
part1 = [3*x[0] + x[1] for x in map(trymachine, inputmachines) if all(x)]
print("Part1: %d" % sum(part1))

#%%
offset = 10000000000000
part2 = [3*x[0] + x[1] 
         for x in map(lambda x: trymachine(x,offset), inputmachines) 
         if all(x)]
print("Part2: %d" % sum(part2))
