# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:09:57 2020

@author: Zijun Huang
"""

import human, dealer
from pokerClasses import Deck, Player, PlayerLinkedList
import AIStrategy as AI

BETTING_OPTIONS = ['fold', 'check', 'call', 'bet', 'raise']
# HANDS = ["Straight Flush", "Four of a Kind", "Full House", "Flush", 
#          "Straight", "Three of a Kind","Two Pairs", "One Pair", "No Pair"]

class Hand(object):
    def __init__(self, player_linked_list, deck, nDeck, n_playing):
        self.max_bet = 0
        self.small_blind = 0
        self.big_blind = 0
        self.deck = deck
        self.nDeck = nDeck
        self.player_linked_list = player_linked_list
        self.node_SB = self.player_linked_list.head.next
        self.node_BB = self.node_SB.next
        self.n_playing = n_playing
        self.n_betting = n_playing
        
        self.ranked_players = []
        self.common_cards = []
        
    def get_blinds(self):
        # get SB and BB
        while True:
            try:
                self.small_blind = int(input('Enter the small blind for this hand: '))
                if self.small_blind > 0:
                    self.big_blind = 2*self.small_blind
                    break
                print('Invalid input. Please enter a positive integer.')
            except ValueError:
                print('Invalid input. Please enter a positive integer.')
        
        player_SB = self.player_linked_list.head.next.player
        player_BB = self.player_linked_list.head.next.next.player
        self.max_bet = self.big_blind
        
        if self.small_blind >= player_SB.money:
            player_SB.all_in = True
            player_SB.money_in_pot = player_SB.money
            self.n_betting -= 1
        else:
            player_SB.money_in_pot = self.small_blind
        
        player_SB.money -= player_SB.money_in_pot
        
        if self.big_blind >= player_BB.money:
            player_BB.all_in = True
            player_BB.money_in_pot = player_BB.money
            self.n_betting -= 1
        else:
            player_BB.money_in_pot = self.big_blind
        
        player_BB.money -= player_BB.money_in_pot
        # if player > 2, make UTG the head
        if self.n_playing > 2:
            node_UTG = self.player_linked_list.head.next.next.next
            self.player_linked_list.update_head(node_UTG)
            
    def deal_holeCards(self):
        node = self.player_linked_list.head.next
        
        while node != self.player_linked_list.tail:
            player = node.player
            player.cards = [self.deck.deal(), self.deck.deal()]
            self.show_player_cards(player)
            
            node = node.next
        
    def pre_flop_bet(self):
        # in heads-up, SB acts first in pre-flop
        self.bet()
    
    def bet_flop(self):
        # in heads-up, BB acts first in post-flop
        # otherwise, SB acts first in post-flop        
        if self.n_playing == 2:
            self.player_linked_list.update_head(self.node_BB)
        else:
            self.player_linked_list.update_head(self.node_SB)
        
        print(self.player_linked_list.count_nodes())
        
        self.bet()
    
    def bet_turn(self):
        self.bet_post_flop()
        
    def bet_river(self):
        self.bet_post_flop()
    
    def bet_post_flop(self):
        if self.n_playing > 2:
            node = self.player_linked_list.head.next
            while node.player.position != "SB":
                node = node.next
            self.player_linked_list.update_head(node)
            
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
        self.common_cards.append(self.deck.deal())
        
    def bet(self):
        '''
        get bets in player_linked_list, assuming it's already in the right order
        '''
        if self.n_betting < 2:
            return
        
        node = self.player_linked_list.head.next
        while node != self.player_linked_list.tail:
            player = node.player
            if player.folded:
                print(player.name + ' has already folded, with '
                      + str(player.money_in_pot) + ' in the pot')
            elif player.all_in:
                print(player.name + ' has been all in, with '
                      + str(player.money_in_pot) + ' in the pot')
            else:
                #TODO
                #if all others have folded, this player automatically wins
                
                print(player.name + '\'s turn, who has '
                      + str(player.money_in_pot) + ' betted in the pot and '
                      + str(player.money) + ' left in the pocket.', end=' ')
                if player.is_AI:
                    bet, amount = AI.bet(player, self.max_bet, 
                                         self.common_cards, self.big_blind)
                else:
                    bet, amount = human.bet(player, self.max_bet)
                    #bet, amount = self.bet_human(player)
                
                print(player.name+' chose to '+bet+', adding ' + str(amount))
                
                self.implement_bet(node, bet, amount)
                print(player.name + ' has '+ str(player.money_in_pot) 
                      + ' in the pot, and has ' + str(player.money)
                      + ' left.')
                                    
            node = node.next   
    
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
            self.max_bet = player.money_in_pot
            self.player_linked_list.update_head(node)
            
    def showdown(self):
        node = self.player_linked_list.head.next
        while node != self.player_linked_list.tail:
            player = node.player
            if player.in_hand:
                self.show_player_best_hand(player)
            node = node.next

    def calculate(self):
        node = self.player_linked_list.head.next
        while node != self.player_linked_list.tail:
            player = node.player
            dealer.update_best_hand(player, self.common_cards)
            player.score = dealer.calculate_score(player.best_hand_type, \
                                                  player.best_hand)
            node = node.next

    def rank_players(self):
        players = []
        node = self.player_linked_list.head.next
        while node != self.player_linked_list.tail:
            players.append(node.player)
            node = node.next
            
        self.ranked_players = sorted(players, key=lambda p: p.score, reverse=True)
    
    def distribute(self):
        '''
        distribute main pot and any side pot
        '''
        self.rank_players()
        dealer.distribute(self.ranked_players)
       
    def show_player_cards(self, player):
        cards = ', '.join([card.__repr__() for card in player.cards])
        print(player.name + ' has ' + cards)
    
    def show_player_best_hand(self, player):
        tp = player.best_hand_type
        hd_string = ','.join([c.__repr__() for c in player.best_hand])
        
        print(player.name + '\'s best hand is a '  + tp 
              + ': ' + hd_string)
    
    def show_all_players_money(self):
        node = self.player_linked_list.head.next
        while node != self.player_linked_list.tail:
            self.show_player_money(node.player)
            node = node.next
    
    def show_player_money(self, player):
        print(player.name + ' has ' + str(player.money) + '.')

    def show_common_cards(self):
        print('Cards on the table are: ' 
              + ','.join(card.__repr__() for card in self.common_cards))
    
    def post_hand_update(self):
        n_remains = 0
        
        node = self.player_linked_list.head.next
        while node != self.player_linked_list.tail:
            p = node.player
            if p.money <= 0:
                p.in_game = p.in_hand = False
            else:
                n_remains += 1
                p.in_game = p.in_hand = True
                
            p.all_in = p.folded = False
            p.money_in_pot = p.score = 0
            p.best_hand = []
            p.best_hand_type = None
            p.cards = []
            
            node = node.next
    
        # appoint the next live player to the left of last SB player
        # to be the next SB
        if n_remains > 1:
            self.player_linked_list.update_head(self.node_SB)
            self.player_linked_list.print_nodes()
            
            self.node_SB.player.position = "TBC"
            node = self.node_SB.next
            while not node.player.in_game:
                node = node.next
            
            node.player.position = "SB"
            print(node.player.name + " is the next SB" 
                  + "=> pos = " + node.player.position)
            
            self.player_linked_list.print_nodes()
        return n_remains
    
class Texas_Holdem_Game(object):
    def __init__(self, n_human, n_AI, money0, nDeck=1):
        self.n_human = n_human
        self.n_AI = n_AI
        self.money0 = money0
        self.blinds = None
        self.hand_idx = 1
        
        self.nDeck = nDeck
        self.deck = None # get one new deck for each hand
        
        self.all_players = []
        self.n_playing = n_human + n_AI
        self.prev_SB_player = None
        
        for i in range(n_human):
            self.all_players.append(self.init_human(i))
        for i in range(n_AI):
            self.all_players.append(self.init_AI(i))
       
  
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
        #random.shuffle(self.all_players)
        
        print('Game has started.')
        # appoint the SB position
        self.prev_SB_player = self.all_players[0]
        self.all_players[0].position = "SB"
        print(self.all_players[0].name + ' has position of ' + self.all_players[0].position)
        
        while self.n_playing > 1:
            print('Playing hand No.' + str(self.hand_idx))
            player_linked_list = self.seat_players(self.all_players)
            self.update_position(player_linked_list)
            player_linked_list.print_nodes()
            
            self.play_one_hand(player_linked_list)
            
            print('Hand No. ' + str(self.hand_idx) + ' has ended.')
            print(str(self.n_playing) + ' player(s) remaining.')
            
            self.hand_idx += 1
            
        self.end_game()
        
    def seat_players(self, players):
        '''
        returns a doubly linked list of the remaining players in players
        '''
        remaining_players = []
        
        for player in players:
            if player.money <= 0:
                player.in_game = player.in_hand = False
            if player.in_game:
                player.in_hand = True
                remaining_players.append(player)
                
        player_linked_list = PlayerLinkedList(remaining_players)
        
        return player_linked_list
          
    def update_position(self, player_linked_list):
        # find "SB" and make it head.next, then update position of the rest
        node = player_linked_list.head.next
        while node != player_linked_list.tail:
            if node.player.position == "SB":
                player_linked_list.update_head(node)
                node.next.player.position = "BB"
                if self.n_playing > 2:
                    node.next.next.player.position = "UTG"
                break
            node = node.next
        
        n = player_linked_list.count_nodes()
        node = player_linked_list.tail.prev
        
        for _ in range((n-1)//3):
            node.player.position = "LP" # late position
            node = node.prev
        
        for _ in range(n-3-(n-1)//3):
            node.player.position = "MP" # middle position
            node = node.prev
    
    def play_one_hand(self, player_linked_list):
        # get a new shuffled deck for each hand
        self.deck = Deck()
        self.deck.shuffle()
        hand = Hand(player_linked_list, self.deck, self.nDeck, self.n_playing)
        
        hand.get_blinds()
        
        hand.deal_holeCards()
        hand.pre_flop_bet()
        
        print('hand.n_betting is :' + str(hand.n_betting))
        hand.deal_flop()

        hand.bet_flop()
        
        print('hand.n_betting is :' + str(hand.n_betting))
        hand.deal_turn()
        hand.bet_turn()
        
        print('hand.n_betting is :' + str(hand.n_betting))
        hand.deal_river()
        hand.bet_river()
        
        hand.calculate()
        
        if hand.n_playing > 1:
            hand.showdown()

        hand.distribute()
        hand.show_all_players_money()
        
        self.n_playing = hand.post_hand_update()
        
        
    def end_game(self):
        print('End of Game.')
 

while True:
    try:
        n_player = int(input('Enter number of players (1 < n < 11): '))
        if 1 < n_player < 11:
            break
        else:
            print('Invalid input. Please enter an integer between 1 and 11')
    except ValueError:
        print('Invalid input. Please enter a integer larger than 1')
              
while True:
    try:
        n_human = int(input('Enter the number of human players (0 < n < ' 
                            + str(n_player+1) + '): '))
        break
    except ValueError:
        print('Invalid input. Please enter an integer between 0 and ' 
              + str(n_player+1) +' :')

while True:
    try:
        money0 = int(input('Enter the amount of money each player has (> 0): '))
        if money0 > 0:
            break
        print('Invalid input. Please enter a positive integer.')
    except ValueError:
        print('Invalid input. Please enter a positive integer.')

game = Texas_Holdem_Game(n_human, n_player-n_human, money0)
game.start_game()








