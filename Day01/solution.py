# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:22:25 2023

@author: ishuwa.sikaneta
"""

#%%
inputFile1 = r"C:\Users\ishuwa.sikaneta\local\src\Advent2023\Day01\input1.txt"

#%% 
with open(inputFile1, "r") as f:
    fields = f.read().split("\n")

#%%
def getInt(c):
    try:
        return int(c)
    except ValueError:
        return None
    
def toNumber(x):
    return int(x[0])*10 + int(x[-1])

#%%
print("Solution part-1: %d" % sum([toNumber(list(filter(getInt,f))) 
                                   for f in fields]))

#%% Part 2
keyd = {"one": "1", 
        "two": "2", 
        "three": "3", 
        "four": "4", 
        "five": "5", 
        "six": "6", 
        "seven": "7", 
        "eight": "8", 
        "nine": "9"}
    
#%%
def repNString(fld):   
    nfld = fld[::-1]
    index = [(fld.index(key),key) for key in keyd.keys() if key in fld]
    if len(index) != 0:
        mykeymin = min(index, key=lambda x: x[0])[1]
        fld = fld.replace(mykeymin, keyd[mykeymin], 1) 
    
    index = [(nfld.index(key[::-1]),key) for key in keyd.keys() 
             if key[::-1] in nfld]
    if len(index) != 0:
        mykeymin = min(index, key=lambda x: x[0])[1]
        nfld =  nfld.replace(mykeymin[::-1], keyd[mykeymin], 1) 
        
    return fld + nfld[::-1]

#%%
inputFile2 = r"C:\Users\ishuwa.sikaneta\local\src\Advent2023\Day01\input2.txt"

with open(inputFile2, "r") as f:
    fields = f.read().split("\n")
    
fields = map(repNString, fields)

print("Solution part-2: %d" % sum([toNumber(list(filter(getInt,f))) 
                                   for f in fields]))