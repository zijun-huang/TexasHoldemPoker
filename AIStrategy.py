# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 16:51:18 2020

@author: Zijun Huang
"""

'''
default probabilities:
    https://en.wikipedia.org/wiki/Poker_probability
preflop chart ref:
    https://www.888poker.com/magazine/strategy/20-poker-charts
'''

import dealer
from pokerClasses import Deck

CHART = [["" for _ in range(15)] for _ in range(15)]
for i in range(2, 15):
    for j in range(i, 15):
        tmp = str(16-i) + ',' + str(16-j) + ','
        if i == j:
            CHART[i][j] = tmp + 'o'
        else:
            CHART[i][j] = tmp + 's'
            CHART[j][i] = tmp + 'o'

PROBs = {"Straight Flush":0.000311, "Four of a Kind":0.00168, 
         "Full House":0.026, "Flush":0.0303, "Straight":0.0462,
         "Three of a Kind":0.0483,"Two Pairs":0.235, "One Pair":0.438, 
         "No Pair":0.174}

UTG_list = CHART[2][2:] + CHART[3][2:7] + CHART[4][2:7] + \
    CHART[5][2:3] + CHART[5][5:7] + CHART[6][2:3] + CHART[6][6:8] + \
        [CHART[i][i] for i in range(7,12)] + CHART[10][11:12]

HJ_list = UTG_list + CHART[3][7:9] + CHART[4][7:8] + CHART[5][3:5] + \
    CHART[5][7:8] + [CHART[i][i+1] for i in range(7,10)] + \
        [CHART[11][12], CHART[12][12]]

CO_list = HJ_list + CHART[3][9:12] + [CHART[4][8], CHART[5][8]] \
    + CHART[6][3:6] + [CHART[i][i+2] for i in range(6,10)]

BTN_list = CO_list + CHART[3][-3:] + CHART[4][9:12] + [CHART[5][9]] + \
    CHART[6][9:11] + CHART[7][2:7] + CHART[7][10:11] + \
        [CHART[i][2] for i in range(8,13)] + [CHART[8][7], CHART[8][11]] + \
            [CHART[10][12], CHART[11][13], CHART[12][13]]

SB_list = BTN_list + CHART[4][-3:] + CHART[5][-5:] + CHART[6][-4:] + \
    CHART[7][11:13] + CHART[8][3:7] + CHART[8][12:13] + CHART[9][3:9] + \
        CHART[9][12:14] + CHART[10][3:5] + CHART[10][8:10] + [CHART[10][13]]\
            + CHART[11][3:5] + CHART[11][9:11] + [CHART[12][3]] + \
                CHART[12][10:12] + [CHART[13][2], CHART[14][2]] + \
                    [CHART[i][-1] for i in range(11,14)]

#['SB', 'BB', 'UTG', 'MP','LP' ]
POSITION_HAND = {'UTG': set(UTG_list), 'MP': set(CO_list), 'LP': set(BTN_list),
              'SB': set(SB_list), 'BB': set(SB_list)}

def pre_flop_bet(player, max_bet, big_blind):
    # return bet
    ranks = sorted([card.rank for card in player.cards], reverse = True)
    cur_hand = ','.join([str(r) for r in ranks])
    if player.cards[0].suit == player.cards[1].suit:
        cur_hand += ',s'
    else:
        cur_hand += ',o'
        
    cur_hand_set = POSITION_HAND[player.position]
    if cur_hand not in cur_hand_set:
        return "fold", 0
    
    # preflop cards are good enough
    if player.money_in_pot == max_bet:
        return 'check', 0
    else:
        return 'call', 0
    
def bet(player, max_bet, common_cards, big_blind):
    print(player.name + ' is thinking...')
    
    if not common_cards:
        return pre_flop_bet(player, max_bet, big_blind)
    
    # simulation
    win_chance = simulate(player, common_cards)
    print('simulated winning probability is {:.2%}'.format(win_chance))
    if win_chance < .40:
        return "fold", 0
    elif win_chance < .80:
        if player.money_in_pot < max_bet:
            return 'call', max_bet-player.money_in_pot
        else:
            return 'check', 0
    else:
        return 'raise', max_bet+big_blind-player.money_in_pot

def simulate(player, common_cards, n_sims=50000):
    deck = Deck()
    
    cards = player.cards + common_cards
    for card in cards:
        deck.remove_card(card)

    type_count = {tp:0 for tp in dealer.HANDS}
    sims_wins = 0
    for _ in range(n_sims):
        deck.shuffle()
        simulated_cards = []
        
        for _ in range(2 + 5 - len(common_cards)):
            simulated_cards.append(deck.deal())
            
        my_cards = player.cards + common_cards + simulated_cards[2:]
        my_hand_type, my_hand = dealer.find_best_hand(my_cards)
        my_score = dealer.calculate_score(my_hand_type, my_hand)
        type_count[my_hand_type] += 1
        
        op_cards = common_cards + simulated_cards
        op_hand_type, op_hand = dealer.find_best_hand(op_cards)
        op_score = dealer.calculate_score(op_hand_type, op_hand)
        type_count[op_hand_type] += 1
        
        if my_score >= op_score:
            sims_wins += 1
            
        for card in simulated_cards:
            deck.add_card(card) 
    
    for tp in type_count:
        msg = tp + ': {:.4%}'
        print(msg.format(type_count[tp]/(2*n_sims)))
        
    return sims_wins/n_sims

    
def eval_hand_strength(player, common_cards):
    #TODO
    pass
    
def detect_op_bluff(player, common_cards, prev_bets):
    #TODO
    pass

def can_bluff(player, common_cards):
    #TODO
    return False
    





 