# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:35:18 2020

@author: Zijun Huang
"""

import random

SUITS = {'spades':chr(9828),'hearts':chr(9829),
         'diamonds': chr(9830),'clubs':chr(9831)}

RANKS = [i for i in range(2, 15)]
RANK_NAME = ['NA', 'NA'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']

#BETTING_OPTIONS = ['fold', 'check', 'bet', 'call']

class Card(object):
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit.lower()
    
    def __repr__(self):
        return '[{:s}{:s}]'.format(RANK_NAME[self.rank], SUITS[self.suit])
              
class Deck(object):
    
    def __init__(self, nDeck=1):
        # standard game: 1 deck per hand
        self.nDeck = nDeck
        self.cards = [Card(rank, suit) for suit in SUITS 
                                      for rank in RANKS]*nDeck
        self.card_set = set(self.cards)

    def __repr__(self):
        return 'a deck with {:d} remaining cards'.format(len(self.cards))
    
    def __len__(self):
        return len(self.cards)
    
    def display_all(self):
        for card in self.cards:
            print(card, end=' ')
    
    def shuffle(self):
        random.shuffle(self.cards)
        #print('Deck has been shuffled.')
    
    def deal(self):
        card = self.cards.pop(0)
        self.card_set.remove(card)
        return card
            
    def discard(self):
        self.cards.deal()
        
    def remove_card(self, card):
        '''
        removes card in deck, return False if card not found in deck
        '''
        for i in range(len(self.cards)):
            cur_card = self.cards[i]
            if cur_card.rank == card.rank and cur_card.suit == card.suit:
                self.cards.pop(i)
                self.card_set.remove(cur_card)
                return True
            
        return False
    
    def add_card(self, card):
        '''
        add card to deck. Return False if card is already in deck
        '''
        if card not in self.card_set:
            self.cards.append(card)
            self.card_set.add(card)
            return True
         
        return False
    
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
        self.best_hand = []
        self.best_hand_type = None
        
        self.cards = []
        
        #TODO
        self.position = "TBC" 
        #['SB', 'BB', 'UTG', 'MP','LP' ]
    
    def __repr__(self):
        return 'player {:s} with {:d} in the pocket'.format(self.name, 
                                                            self.money)
    
    #def observeFacialExpression(self)    
    #def says(self)
    #def action(self)
    
    
class ListNode(object):
    def __init__(self, player, prev=None, next=None):
        self.player = player
        self.prev = prev
        self.next = next

class PlayerLinkedList(object):
    def __init__(self, players):
        self.players = players
        self.head = ListNode(None)
        self.tail = ListNode(None)
        
        cur = self.head
        for player in players:
            node = ListNode(player, prev = cur)
            cur.next = node
            cur = cur.next
        
        cur.next = self.tail
        self.tail.prev = cur
    
    def update_head(self, node):
        # update to: head -> node ->...-> tail
        
        self.tail.prev.next = self.head.next
        self.head.next.prev = self.tail.prev
        self.tail.prev = node.prev
        node.prev.next = self.tail
        node.prev = self.head
        self.head.next = node
    
    def count_nodes(self):
        n = 0
        node = self.head.next
        while node != self.tail:
            n += 1
            node = node.next
            
        return n
    
    def make_list(self):
        player_list = []
        node = self.head.next
        while node != self.tail:
            player_list.append(node.player)
            node = node.next
        
        return player_list
    
    def print_nodes(self):
        player_list = self.make_list()
        
        print(', '.join([p.name + ":" + p.position for p in player_list]))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        