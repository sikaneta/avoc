# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 08:31:23 2023

@author: ishuwa.sikaneta
"""
import json
import requests
from functools import cmp_to_key
from collections import defaultdict

#%%
avocjson = r"C:\Users\ishuwa.sikaneta\local\src\avoc.json"
with open(avocjson, "r") as f:
    cookies = json.loads(f.read())
session = requests.session()
scook = requests.utils.cookiejar_from_dict(cookies)
session.cookies.update(scook)
resp = session.get("https://adventofcode.com/2023/day/7/input")

#%%
lines = resp.text.split('\n')[:-1]

testlines = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".split('\n')[1:-1]

#%% Functions
class player:
    hands = ["five-of-a-kind",
             "four-of-a-kind",
             "full-house",
             "three-of-a-kind",
             "two-pair",
             "pair",
             "high-card"]
    
    cards = "AKQJT98765432"
    tiebreak = "AKQJT98765432"
    
    def __init__(self, record):
        deal, bet = record.split()
        self.bet = int(bet)
        self.deal = deal
        self.call, _ = self.getHand(deal)
        
    def getHand(self, deal):
        hands = self.hands
        hand = defaultdict(list)
        for x in deal:
            hand[x].append(x)
    
        nkeys = len(hand.keys())
        if nkeys == 5:
            call = hands[6]
        elif nkeys == 4:
            call = hands[5]
        elif nkeys == 3:
            if any([len(v)==3 for _,v in hand.items()]):
                call = hands[3]
            else:
                call = hands[4]
        elif nkeys == 2:
            if any([len(v)==4 for _,v in hand.items()]):
                call = hands[1]
            else:
                call = hands[2]
        else:
            call = hands[0]
            
        return call, deal
    
    def __lt__(self, other):
        return self.isLessThan((self.call, self.deal), (other.call, other.deal))
            
    def isLessThan(self, me, you):
        tiebreak = self.tiebreak
        hands = self.hands
        scall, sdeal = me
        ocall, odeal = you
        if hands.index(scall) > hands.index(ocall):
            return True
        elif hands.index(scall) < hands.index(ocall):
            return False
        
        for k in range(5):
            if tiebreak.index(sdeal[k]) > tiebreak.index(odeal[k]):
                return True
            elif tiebreak.index(sdeal[k]) < tiebreak.index(odeal[k]):
                return False
            
        raise ValueError
            
class playerNewRules(player):
    tiebreak = "AKQT98765432J"
    def __init__(self, record):
        deal, bet = record.split()
        self.bet = int(bet)
        self.deal = deal
        
        if 'J' not in deal:
            self.call, _ = self.getHand(deal)
            self.callhand = self.deal
        else: 
            self.options = sorted([self.getHand(deal.replace('J',c)) 
                                   for c in self.cards],
                                  key=cmp_to_key(self.compare))
            self.call = self.options[-1][0]
            self.callhand = self.options[-1][-1]
            
    def compare(self, me, you):
        if self.isLessThan(me, you):
            return -1
        scall, sdeal = me
        ocall, odeal = you
        if scall == ocall and sdeal == odeal:
            return 0
        else:
            return 1
        
#%%
mylines = lines

#%%
game = sorted([player(x) for x in mylines])
print("Part1: %d" % sum([g.bet*(k+1) for k,g in enumerate(game)]))

#%%
ngame = sorted([playerNewRules(x) for x in mylines])
print("Part2: %d" % sum([g.bet*(k+1) for k,g in enumerate(ngame)]))

