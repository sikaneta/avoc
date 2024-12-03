# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
import re

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/3/input")

#%%
lines = resp.text

testlines = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

#%%
def mul(x,y):
    return x*y

#%%
pool = lines
def run_compute(pool):
    re_str = "mul[(][0-9]{1,3},[0-9]{1,3}[)]"
    return sum([eval(atom) for atom in re.findall(re_str, pool)])

#%%
part1 = run_compute(pool)
print("Part 1: %d" % part1)

#%%
testlines = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

#%%
part2 = map(run_compute, [re.split("don't[(][)]", x)[0] for x in re.split("do[(][)]", testlines)])
print("Part 2: %d" % sum(part2))
