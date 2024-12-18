# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
#%%
import json
import requests
import queue
from functools import reduce
import re

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/17/input")

#%%
prod = resp.text[:-1]

#%%
test = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""[1:-1]

test2 = """
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""[1:-1]
#%%
def parse(prog):
    data = [int(x) for x in re.findall("[0-9]*", prog) if x ]
    return {
        "A": data[0],
        "B": data[1],
        "C": data[2],
        }, data[3:]
    
def operand(op, register):
    if op in [0,1,2,3]:
        return op
    elif op ==4:
        return register["A"]
    elif op ==5:
        return register["B"]
    elif op ==6:
        return register["C"]
    else:
        return None
    
def operate(opcode, op, pointer, register, output):
    if opcode == 0:
        val = int(register["A"]/(2**operand(op,register)))
        register["A"] = val
    elif opcode == 1:
        val = register["B"] ^ op
        register["B"] = val
    elif opcode == 2:
        val = operand(op,register) % 8
        register["B"] = val
    elif opcode == 3:
        if register["A"] != 0:
            return op
    elif opcode == 4:
        val = register["B"] ^ register["C"]
        register["B"] = val
    elif opcode == 5:
        val = (operand(op,register) % 8)
        output.append("%d" % val)
    elif opcode == 6:
        val = int(register["A"]/(2**operand(op,register)))
        register["B"] = val
    elif opcode == 7:
        val = int(register["A"]/(2**operand(op,register)))
        register["C"] = val
    return pointer + 2
    
#%%
def runProg(reg, prog, Aval = None):
    if Aval is not None: 
        reg["A"] = Aval 
    pointer = 0
    output = []
    while pointer < len(prog):
        pointer = operate(prog[pointer], prog[pointer + 1], pointer, reg, output)
        
    return output
    
reg, prog = parse(prod) 
print("Part1: %s" % ",".join(runProg(reg, prog)))
    
#%%
def fork(q, reg, prog, res):
    N = len(prog)
    x = q.get()
    m = len(x)
    Aval = sum([c*8**(N-k) for k,c in enumerate(x)])
    if len(x) == N:
        res.append(int(Aval/8))
        return
    dd = [int(runProg(reg, prog, Aval=Aval + k*(8**(N-m)))[-(m+1)]) 
          for k in range(8)]
    
    for k,y in enumerate(dd):
        if y == prog[-(m+1)]:
            q.put(x + [k])

#%%
q = queue.Queue()
q.put([3])

#%%
counter = 0
res = []
while not q.empty():
    fork(q, reg, prog, res)
    counter += 1
    if counter % 100 == 1:
        print(q.qsize())
    

#%%
part2 = min(res)
print("Part2: %d" % part2)

