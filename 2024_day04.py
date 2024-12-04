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
resp = session.get("https://adventofcode.com/2024/day/4/input")

#%%
lines = resp.text.split('\n')[:-1]

testlines = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".split('\n')[1:-1]

#%%
text = lines
data = np.zeros((len(text)+3, len(text[0])+3), dtype = np.complex64)

rep = {'X': 1, 'M': 2, 'A': 3, 'S': 4}
for m,line in enumerate(text):
    for n,c in enumerate(line):
        try:
            data[m,n] = rep[c]*np.exp(2*np.pi*1j*rep[c]/4)
        except KeyError:
            pass

ft_data = np.fft.fft2(data)

#%%
def detections(ft_data, seq):
    flt = [np.zeros((4,4), dtype=np.complex64),
           np.zeros((4,4), dtype=np.complex64),
           np.zeros((4,4), dtype=np.complex64),
           np.zeros((4,4), dtype=np.complex64)]
    flt[0][:,0] = seq
    flt[1][0,:] = seq
    flt[2] = flt[2] + np.diag(seq)
    flt[3] = np.fliplr(flt[3] + np.diag(seq))
    return sum([convolve(ft_data, f, 29.9)[0] for f in flt])
    
def convolve(ft_data, flt, threshold, N=4):
    ft_flt = np.fft.fft2(flt*np.exp(2*np.pi*1j*flt/N), ft_data.shape)
    flt_data = np.abs(np.fft.ifft2(ft_data*np.conj(ft_flt)))
    return len(np.argwhere(flt_data > threshold)), flt_data 

#%%
seq = np.arange(1,5)
print("Part 1: %d" % (detections(ft_data, seq) +
                      detections(ft_data, np.flipud(seq))))

#%%
rep = {'M': 1, 'A': 2, 'S': 3}
data2 = np.zeros_like(data)
for m,line in enumerate(text):
    for n,c in enumerate(line):
        try:
            data2[m,n] = rep[c]*np.exp(2*np.pi*1j*rep[c]/3)
        except KeyError:
            pass

ft_data2 = np.fft.fft2(data2)
flt = np.array([[1,0,3],[0,2,0],[1,0,3]])
#%%
flts = [flt,np.fliplr(flt), flt.T, np.flipud(flt.T)]
part2 = [convolve(ft_data2, f, 23.9, N=3)[0] for f in flts]
print("Part 2: %d" % sum(part2))
