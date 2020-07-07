# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:40:32 2020

@author: Zijun Huang
"""

import operator, random, time
from functools import reduce

import dealer
from pokerClasses import Deck

def kCn(n, k):
    '''
    returns number of combinaiton of choosing k elements from n elements
    '''
    if k > n:
        return 0
    if k > n//2:
        k = n-k
    
    numerator = reduce(operator.mul, range(n, n-k, -1), 1)
    denominator = reduce(operator.mul, range(1, k+1, 1), 1)
    
    return numerator // denominator
    

def simulate(n_sims=3*10**6): #10**8
    deck = Deck()
    type_count = {tp:0 for tp in dealer.HANDS}
    
    for _ in range(n_sims):
        cards = random.sample(deck.cards, 7)
        best_type, _ = dealer.find_best_hand(cards)
        type_count[best_type] += 1
    
    for tp in type_count:
        msg = tp + ': {:.6%}'
        print(msg.format(type_count[tp]/(n_sims)))
    
    return type_count

if __name__ == '__main__':
    t0 = time.time()
    type_count = simulate()  
    t1 = time.time()
    print('{:.2f}s has passed'.format(t1-t0))