# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""

#%%
import json
import requests

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc2024.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2024/day/24/input")

#%%
prod = resp.text[:-1].split('\n\n')

#%%
test1 = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""[1:-1].split('\n\n')
    
#%%
mystuff = prod
mcmp = dict()
for y in mystuff[0].split('\n'):
    x = y.split(': ')
    mcmp[x[0]] = {"fn": "I", 
                  "inputs": (int(x[1]),)}
    
for y in mystuff[1].split('\n'):
    x = y.split(' ')
    mcmp[x[-1]] = {"fn": x[1],
                   "inputs": (x[0], x[2])}
 
fdict = {
    "OR": lambda x,y: x|y,
    "XOR": lambda x,y: x^y,
    "AND": lambda x,y: x&y,
    "I": lambda x: x}

def callfn(mcmp, key):
    item = mcmp[key]
    args = item['inputs']
    if item['fn'] == 'I':
        return item['inputs'][0]
    else: 
        return fdict[item['fn']](callfn(mcmp, args[0]), 
                                 callfn(mcmp, args[1]))
    
#%%
zkeys = sorted([x for x in mcmp.keys() if x[0] == 'z'])
N = len(zkeys)
bits = [callfn(mcmp, z) << (N-k-1) for k,z in enumerate(zkeys[-1::-1])]

#%%
print("Part1: %d" % sum(bits))

#%%
Xin = sorted([k for k,v in mcmp.items() if v['fn'] == 'I' and 'x' in k])
Yin = sorted([k for k,v in mcmp.items() if v['fn'] == 'I' and 'y' in k])
#%%
gates = [
    {
    "xXORkey": {k:v for k,v in mcmp.items() if Xin[0] in v['inputs'] 
                and v['fn'] == 'XOR'},
    "yXORkey": {k:v for k,v in mcmp.items() if Yin[0] in v['inputs'] 
                and v['fn'] == 'XOR'},
    "xANDkey": {k:v for k,v in mcmp.items() if Xin[0] in v['inputs'] 
                and v['fn'] == 'AND'},
    "yANDkey": {k:v for k,v in mcmp.items() if Yin[0] in v['inputs'] 
                and v['fn'] == 'AND'}
    }
]
gates[0]["cout"] = gates[0]["xANDkey"]
gates[0]["sum"] = gates[0]["xXORkey"]

#%%
def tryOption(gate, key, gtype):
    try:
        return {k:v for k,v in mcmp.items()
                if list(gate[key])[0] in v["inputs"]
                and v["fn"] == gtype}
    except IndexError:
        return {}

def findDict(x, gtype):
    return {k:v for k,v in mcmp.items() if x in v['inputs'] 
               and v['fn'] == gtype}
#%%  
mcmp["z08"] = {'fn': 'XOR', 'inputs': ('gvw', 'kgn')} 
mcmp["vvr"] = {'fn': 'OR', 'inputs': ('kwv', 'ctv')}
mcmp["mqh"] = {'fn': 'AND', 'inputs': ('thk', 'wnk')}
mcmp["z39"] = {'fn': 'XOR', 'inputs': ('wnk', 'thk')}
mcmp["z28"] = {'fn': 'XOR', 'inputs': ('djn', 'ptk')}
mcmp["tfb"] = {'fn': 'AND', 'inputs': ('y28', 'x28')}
mcmp["bkr"] = {'fn': 'AND', 'inputs': ('y16', 'x16')}
mcmp["rnq"] = {'fn': 'XOR', 'inputs': ('y16', 'x16')}

#%%
for x,y in zip(Xin[1:], Yin[1:]):
    cin = list(gates[-1]["cout"])[0]
    dd = {
    "xXORkey": {k:v for k,v in mcmp.items() if x in v['inputs'] 
               and v['fn'] == 'XOR'},
    "yXORkey": {k:v for k,v in mcmp.items() if y in v['inputs'] 
               and v['fn'] == 'XOR'},
    "xANDkey": {k:v for k,v in mcmp.items() if x in v['inputs'] 
               and v['fn'] == 'AND'},
    "yANDkey": {k:v for k,v in mcmp.items() if y in v['inputs'] 
               and v['fn'] == 'AND'},
    "cANDkey": {k:v for k,v in mcmp.items() if cin in v['inputs'] 
               and v['fn'] == 'AND'},
    "cXORkey": {k:v for k,v in mcmp.items() if cin in v['inputs'] 
               and v['fn'] == 'XOR'},
    "sum": mcmp[x.replace('x', 'z')]
    }
    dd["pORkey"] = tryOption(dd, "cANDkey", "OR")
    dd["sORkey"] = tryOption(dd, "xANDkey", "OR")
    dd["cout"] = dd["pORkey"]
    gates.append(dd)

""" The gates array is inspected manually for inconsistencies. These
    are recorded in the previous cell. In some cases, the loop fails to
    complete, in other cases, a manual inspection of the out showed the
    inconsistencies"""
#%%
skeys = sorted(["z08", "vvr", "mqh", "z39", "z28", "tfb", "bkr", "rnq"])
print("Part2: %s" % ",".join(skeys))