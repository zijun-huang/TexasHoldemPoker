# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:35:18 2020

@author: Zijun Huang
"""

import random

SUITS = {'spades':chr(9828),'hearts':chr(9829),
         'diamonds': chr(9830),'clubs':chr(9831)}

RANKS = [i for i in range(2, 14)]

#BETTING_OPTIONS = ['fold', 'check', 'bet', 'call']

class Card(object):
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit.lower()
    
    def __repr__(self):
        return '[{:d}{:s}]'.format(self.rank, SUITS[self.suit])
              
class Deck(object):
    
    def __init__(self, nDeck=1):
        # suport multiple standard decks to be used
        self.nDeck = nDeck
        self.cards = [Card(rank, suit) for suit in SUITS 
                                      for rank in RANKS]*nDeck

    def __repr__(self):
        return 'a deck with {:d} remaining cards'.format(len(self.cards))
    
    def __len__(self):
        return len(self.cards)
    
    def display_all(self):
        for card in self.cards:
            print(card, end=' ')
    
    def shuffle(self):
        random.shuffle(self.cards)
        print('Deck has been shuffled.')
    
    def deal(self):
        # try:
        #     return self.cards.pop(0)
        # except IndexError:
        #     print('Cannot get card. Deck is empty')
        
        return self.cards.pop(0)
            
    def discard(self):
        self.cards.deal()
    
class Player(object):
    def __init__(self, name, money, is_AI):
        self.name = name
        self.is_AI = is_AI
        self.money = money
        self.in_game = True
        
        self.in_hand = True
        self.all_in = False
        self.folded = False
        self.money_in_pot = 0
        
        self.score = 0
        self.highest_hand = []
        self.highest_hand_type = None
        
        self.cards = []
    
    def __repr__(self):
        return 'player {:s} with {:d} in the pocket'.format(self.name, 
                                                            self.money)
        
    #def observeFacialExpression(self)    
    #def says(self)
    #def action(self)
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        