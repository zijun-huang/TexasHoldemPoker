# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:09:57 2020

@author: Zijun Huang
"""

import random
from pokerClasses import Deck, Player
import AIStrategy as AI
import dealer

BETTING_OPTIONS = ['fold', 'check', 'call', 'bet', 'raise']
# HANDS = ["Straight Flush", "Four of a Kind", "Full House", "Flush", 
#          "Straight", "Three of a Kind","Two Pairs", "One Pair", "No Pair"]

class ListNode(object):
    def __init__(self, player, prev=None, next=None):
        self.player = player
        self.prev = prev
        self.next = next

class Hand(object):
    def __init__(self, head, deck, nDeck, n_playing):
        self.max_bet = 0
        self.blinds = 0
        self.deck = deck
        self.nDeck = nDeck
        self.head = head
        self.n_playing = n_playing
        self.n_betting = n_playing
        
        self.ranked_players = []
        self.common_cards = []
    
    def get_blinds(self):
        while True:
            try:
                self.blinds = int(input('Enter the blinds for this hand: '))
                if self.blinds >= 0:
                    break
                print('Invalid input. Please enter a non-negative integer.')
            except ValueError:
                print('Invalid input. Please enter a non-negative integer.')
        
        curPlayers = []
        node = self.head.next
        while node:
            player = node.player
            curPlayers.append(player)
            if self.blinds >= player.money:
                player.all_in = True
                player.money_in_pot = player.money
                self.n_betting -= 1
            else:
                player.money_in_pot = self.blinds
                
            player.money -= player.money_in_pot
            self.max_bet = max(self.max_bet, player.money_in_pot)
            node = node.next
            
        print('Players in this hand are: '+
              ', '.join([player.name for player in curPlayers]))
        
    def deal_holeCards(self):
        node = self.head.next
        
        while node:
            player = node.player
            if len(self.deck) < 2:
                self.get_new_deck()
                
            player.cards = [self.deck.deal(), self.deck.deal()]
            self.show_player_cards(player)
            
            node = node.next
        
    def pre_flop_bet(self):
        self.bet()
    
    def deal_flop(self):
        for _ in range(3):
            self.deal()
        
        self.show_common_cards()
            
    def deal_turn(self):
        self.deal()
        self.show_common_cards()
    
    def deal_river(self):
        self.deal()
        self.show_common_cards()
    
    def deal(self):
        if len(self.deck) == 0:
            self.get_new_deck()
                
        self.common_cards.append(self.deck.deal())
        
    def bet(self):
        if self.n_betting < 2:
            return
        
        node = self.head.next
        while node:
            player = node.player
            if player.folded:
                print(player.name + ' has already folded, with '
                      + str(player.money_in_pot) + ' in the pot')
            elif player.all_in:
                print(player.name + ' has been all in, with '
                      + str(player.money_in_pot) + ' in the pot')
            else:
                print(player.name + '\'s turn, who has '
                      + str(player.money_in_pot) + ' betted in the pot and '
                      + str(player.money) + ' left in the pocket.', end=' ')
                if player.is_AI:
                    bet, amount = AI.bet(player, self.max_bet, self.common_cards)
                else:
                    bet, amount = self.bet_human(player)
                
                self.implement_bet(node, bet, amount)
                print(player.name + ' has '+ str(player.money_in_pot) 
                      + ' in the pot, and has ' + str(player.money)
                      + ' left.')
                                    
            node = node.next   
    
    def bet_human(self, player):
        '''
        returns bet, amount
        '''
        while True:
            try:
                if self.max_bet == player.money_in_pot:
                    if player.money > 0:
                        options = ['fold', 'check', 'bet']
                    else:
                        options = ['fold', 'check']
                else:
                    if player.money > self.max_bet - player.money_in_pot:
                        options = ['fold', 'call', 'raise']
                    else:
                        options = ['fold', 'call']
                
                bet = input('Enter your decision. Your current options are '
                            + str(options)+'\n')
                if bet in options:
                    break
                print('Please choose only from the available options '+
                          'and try again.')
            except ValueError:
                print('Please choose only from the available options '+
                          'and try again.')
        
        if bet == 'fold' or bet == 'check':
            return bet, 0
        
        if bet == 'call':
            return bet, min(player.money, self.max_bet - player.money_in_pot)
        
        if bet == 'bet' or 'raise':
            while True:
                try:
                    minBet = self.max_bet-player.money_in_pot +1
                    amount = int(input('Enter the amount you want to put down '+
                                 '(minimum is ' + str(minBet) + '): '))
                    if amount >= minBet:
                        break
                    print('Invalid input. Please enter an integer '+
                          'not smaller than ' + str(minBet))
                except ValueError:
                    print('Invalid input. Please enter an integer '+
                          'not smaller than ' + str(minBet))
        
        return bet, amount
    
    def showdown(self):
        node = self.head.next
        while node:
            player = node.player
            if player.in_hand:
                self.show_player_best_hand(player)
            node = node.next

    def calculate(self):
        node = self.head.next
        while node:
            player = node.player
            dealer.find_best_hand(player, self.common_cards)
            dealer.calculate_score(player)
            node = node.next
    
    def rank_players(self):
        players = []
        node = self.head.next
        while node:
            players.append(node.player)
            node = node.next
            
        self.ranked_players = sorted(players, 
                                     key=lambda p: p.score, reverse=True)
    
    def distribute(self):
        '''
        distribute main pot and any side pot
        '''
        self.rank_players()
        dealer.distribute(self.ranked_players)
        
    def implement_bet(self, node, bet, amount):
        player = node.player
        if bet == 'fold':
            player.folded = True
            self.n_playing -= 1
            self.n_betting -= 1
            return
        if bet == 'check':
            assert(player.money_in_pot == self.max_bet)
            return
        
        # call, bet, raise
        if amount >= player.money:
            player.all_in = True
            player.money_in_pot += player.money
            player.money = 0
            self.n_betting -= 1
        else:
            player.money_in_pot += amount
            player.money -= amount
        
        # check if the bet increases the bar, if so, update player linked list
        if self.max_bet < player.money_in_pot:
        #if bet == 'bet' or bet == 'raise':
            self.max_bet = player.money_in_pot
            
            tail = node
            while tail.next:
                tail = tail.next
            
            tail.next = self.head.next
            tail.next.prev = tail
            self.head.next = node
            node.prev.next = None
            node.prev = None
            
    def show_player_cards(self, player):
        cards = ', '.join([card.__repr__() for card in player.cards])
        print(player.name + ' has ' + cards)
    
    def show_player_best_hand(self, player):
        tp = player.best_hand_type
        hd_string = ','.join([c.__repr__() for c in player.best_hand])
        
        print(player.name + '\'s best hand is a '  + tp 
              + ': ' + hd_string)
    
    def show_all_players_money(self):
        node = self.head.next
        while node:
            self.show_player_money(node.player)
            node = node.next
    
    def show_player_money(self, player):
        print(player.name + ' has ' + str(player.money) + '.')

    def show_common_cards(self):
        print('Cards on the table are: ' 
              + ','.join(card.__repr__() for card in self.common_cards))

    def get_new_deck(self):
        self.deck.extend(Deck(self.nDeck))
        self.deck.shuffle()
    
    
class Texas_Holdem_Game(object):
    def __init__(self, n_human, n_AI, money0, nDeck = 5):
        self.n_human = n_human
        self.n_AI = n_AI
        self.money0 = money0
        self.blinds = None
        self.hand_idx = 1
        
        self.nDeck = nDeck
        self.deck = Deck(nDeck) # unshuffled yet
        
        self.all_players = []
        self.n_playing = n_human + n_AI

        for i in range(n_human):
            self.all_players.append(self.init_human(i))
        for i in range(n_AI):
            self.all_players.append(self.init_AI(i))
        
    def seat_players(self, players):
        # doubly linked list: head <-> player0 <-> player1 .. <-> player n-1
        head = ListNode(None)
        last = head
        for player in players:
            if player.money < 0:
                player.in_game = player.in_hand = False
                
            if player.in_game:
                p = ListNode(player, prev=last)
                last.next = p
                last = p
        
        return head
            
    def init_human(self, i):
        while True:
            try:
                name = input('Enter the name of human player No.'
                             + str(i+1)+':\t')                
                return Player(name, self.money0, False)
            
            except ValueError:
                print('Invalid input. Please try again.')
    
    def init_AI(self, i):
        return Player("AI"+str(i+1), self.money0, True)
    
    def start_game(self):
        random.shuffle(self.all_players)
        self.deck.shuffle()
        
        print('Game has started.')
        
        while self.n_playing > 1:
            print('Playing hand No.' + str(self.hand_idx))
            head = self.seat_players(self.all_players)
            self.play_one_hand(head)
            self.post_hand_update(head)
            print('Hand No. ' + str(self.hand_idx) + ' has ended.')
            print(str(self.n_playing) + ' player(s) remaining.')
            
        self.end_game()
    
    def play_one_hand(self, head):
        hand = Hand(head, self.deck, self.nDeck, self.n_playing)
        
        hand.get_blinds()
        
        hand.deal_holeCards()
        hand.pre_flop_bet()
        
        print('hand.n_betting is :' + str(hand.n_betting))
        hand.deal_flop()
        hand.bet()
        
        print('hand.n_betting is :' + str(hand.n_betting))
        hand.deal_turn()
        hand.bet()
        
        print('hand.n_betting is :' + str(hand.n_betting))
        hand.deal_river()
        hand.bet()
        
        hand.calculate()
        
        if hand.n_playing > 1:
            hand.showdown()

        hand.distribute()
        hand.show_all_players_money()
        
    def post_hand_update(self, head):
        self.n_playing = 0
        
        node = head.next
        while node:
            p = node.player
            if p.money <= 0:
                p.in_game = p.in_hand = False
            else:
                self.n_playing += 1
                p.in_game = p.in_hand = True
                
            p.all_in = p.folded = False
            p.money_in_pot = p.score = 0
            p.best_hand = []
            p.best_hand_type = None
            p.cards = []
            
            node = node.next

    def end_game(self):
        print('End of Game.')
 

while True:
    try:
        nTotalPlayers = int(input('Enter the number of total players (>1): '))
        if nTotalPlayers > 1:
            break
        else:
            print('Invalid input. Please enter a integer larger than 1')
    except ValueError:
        print('Invalid input. Please enter a integer larger than 1')
              
while True:
    try:
        n_human = int(input('Enter the number of human players (>=1): '))
        break
    except ValueError:
        print('Invalid input. Please enter a positive integer')


while True:
    try:
        money0 = int(input('Enter the starting amount of money every player has (>0): '))
        break
    except ValueError:
        print('Invalid input. Please enter a positive integer.')

game = Texas_Holdem_Game(n_human, nTotalPlayers-n_human, money0)
game.start_game()








