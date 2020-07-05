# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:09:57 2020

@author: Zijun Huang
"""

import random
from pokerClasses import Card, Deck, Player
import AIStrategy as AI
import dealer

BETTING_OPTIONS = ['fold', 'check', 'call', 'bet', 'raise']
HANDS = ["Straight Flush", "Four of a Kind", "Full House", "Flush", 
         "Straight", "Three of a Kind","Two Pairs", "One Pair", "No Pair"]

class ListNode(object):
    def __init__(self, player, prev=None, next=None):
        self.player = player
        self.prev = prev
        self.next = next

class Hand(object):
    def __init__(self, head, deck, nDeck, nActivePlayers):
        self.highestBet = 0
        self.blinds = 0
        self.deck = deck
        self.nDeck = nDeck
        self.head = head
        self.nActivePlayers = nActivePlayers
        
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
                player.allIn = True
                player.moneyBetted = player.money
            else:
                player.moneyBetted = self.blinds
            player.money -= player.moneyBetted
            self.highestBet = max(self.highestBet, player.moneyBetted)
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
        node = self.head.next
        while node:
            player = node.player
            if player.folded:
                print(player.name + ' has already folded, with '
                      + str(player.moneyBetted) + ' in the pot')
            elif player.allIn:
                print(player.name + ' has been all in, with '
                      + str(player.moneyBetted) + ' in the pot')
            else:
                print(player.name + '\'s turn, who has '
                      + str(player.moneyBetted) + ' betted in the pot and '
                      + str(player.money) + ' left in the pocket.', end=' ')
                if player.isAI:
                    bet, amount = AI.bet(player, self.highestBet, self.common_cards)
                else:
                    bet, amount = self.bet_human(player)
                
                self.implement_bet(node, bet, amount)
                print(player.name + ' now has '+ str(player.moneyBetted) 
                      + ' in the pot, and has ' + str(player.money)
                      + ' left in the pocket')
                                    
            node = node.next   
    
    def bet_human(self, player):
        '''
        returns bet, amount
        '''
        while True:
            try:
                if self.highestBet == player.moneyBetted:
                    if player.money > 0:
                        options = ['fold', 'check', 'bet']
                    else:
                        options = ['fold', 'check']
                else:
                    if player.money > self.highestBet - player.moneyBetted:
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
            return bet, min(player.money, self.highestBet - player.moneyBetted)
        
        if bet == 'bet' or 'raise':
            while True:
                try:
                    minBet = self.highestBet-player.moneyBetted +1
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
            if player.inHand:
                self.show_player_cards(player)
            node = node.next

    def calculate(self):
        node = self.head.next
        while node:
            player = node.player
            dealer.find_highest_hand(player, self.common_cards)
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
            self.nActivePlayers -= 1
            return
        if bet == 'check':
            assert(player.moneyBetted == self.highestBet)
            return
        
        # call, bet, raise
        if amount >= player.money:
            player.allIn = True
            player.moneyBetted += player.money
            player.money = 0
        else:
            player.moneyBetted += amount
            player.money -= amount
        
        # check if the bet increases the bar, if so, update player linked list
        if self.highestBet < player.moneyBetted:
        #if bet == 'bet' or bet == 'raise':
            self.highestBet = player.moneyBetted
            
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

    def show_common_cards(self):
        print('Cards on the table are: ' 
              + ','.join(card.__repr__() for card in self.common_cards))

    def get_new_deck(self):
        self.deck.extend(Deck(self.nDeck))
        self.deck.shuffle()
    
class TexasHoldemGame(object):
    def __init__(self, nHumanPlayers, nAIs, startMoney, nDeck = 5):
        self.nHumanPlayers = nHumanPlayers
        self.nAIs = nAIs
        self.startMoney = startMoney
        self.blinds = None
        self.handIdx = 1
        
        self.nDeck = nDeck
        self.deck = Deck(nDeck)
        #self.deck.shuffle()
        
        self.allPlayers = []
        self.nActivePlayers = nHumanPlayers + nAIs
        self.curHandPlayers = []
        
        for i in range(nHumanPlayers):
            self.allPlayers.append(self.initializeHuman(i))
        for i in range(nAIs):
            self.allPlayers.append(self.initializeAI(i))
        
    def seatPlayers(self, players):
        # doubly linked list: head <-> player0 <-> player1 .. <-> player n-1
        
        head = ListNode(None)
        last = head
        for player in players:
            if player.money < 0:
                player.inGame = player.inHand = False
                
            if player.inGame:
                p = ListNode(player, prev=last)
                last.next = p
                last = p
        
        return head
            
    def initializeHuman(self, i):
        while True:
            try:
                name = input('Enter the name of human player No.'
                             + str(i+1)+':\t')                
                return Player(name, self.startMoney, False)
            
            except ValueError:
                print('Invalid input. Please try again.')
    
    def initializeAI(self, i):
        return Player("AI"+str(i+1), self.startMoney, True)
    
    def startGame(self):
        random.shuffle(self.allPlayers)
        self.deck.shuffle()
        
        print('Game has started.')
        
        while self.nActivePlayers > 1:
            print('Playing hand No.' + str(self.handIdx))
            head = self.seatPlayers(self.allPlayers)
            self.playOneHand(head)
            self.postHandUpdate(head)
            break
            
        self.endGame()
    
    def playOneHand(self, head):
        hand = Hand(head, self.deck, self.nDeck, self.nActivePlayers)
        hand.get_blinds()
        hand.deal_holeCards()
        hand.pre_flop_bet()
        
        if hand.nActivePlayers == 1:
            hand.calculate()
            hand.distribute()
            return
        
        hand.deal_flop()
        hand.bet()
        
        if hand.nActivePlayers == 1:
            hand.calculate()
            hand.distribute()
            return
        
        hand.deal_turn()
        hand.bet()
        
        if hand.nActivePlayers == 1:
            hand.calculate()
            hand.distribute()
            return
        
        hand.deal_river()
        hand.bet()
        
        if hand.nActivePlayers == 1:
            hand.calculate()
            hand.distribute()
            return
        
        if hand.nActivePlayers > 1:
            hand.showdown()
        
        hand.calculate()
        hand.distribute()
        
    def postHandUpdate(self, head):
        pass

    def endGame(self):
        print('End of Game, winner is...')
 

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
        nHumanPlayers = int(input('Enter the number of human players (>=1): '))
        break
    except ValueError:
        print('Invalid input. Please enter a positive integer')


while True:
    try:
        startMoney = int(input('Enter the starting amount of money every player has (>0): '))
        break
    except ValueError:
        print('Invalid input. Please enter a positive integer.')

game = TexasHoldemGame(nHumanPlayers, nTotalPlayers-nHumanPlayers, startMoney)
game.startGame()








