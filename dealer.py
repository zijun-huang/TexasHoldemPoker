# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 10:03:57 2020

@author: Zijun Huang
"""

from collections import Counter, defaultdict
from pokerClasses import Card

HANDS = ["Straight Flush", "Four of a Kind", "Full House", "Flush", 
         "Straight", "Three of a Kind","Two Pairs", "One Pair", "No Pair"]

def search_straight_flush(cards):
    '''
    cards: sorted cards by rank high to low
    '''
    # cover low straight flush possibility
    _cards = [card for card in cards]
    for card in cards:
        if card.rank < 14:
            break
        _cards.append(Card(1, card.suit))

    for i in range(len(_cards)-4):
        suit = _cards[i].suit
        ans = [_cards[i]]
        for j in range(i+1,len(_cards)):
            if _cards[j].rank < ans[-1].rank - 1:
                break
            if _cards[j].rank == ans[-1].rank - 1 and _cards[j].suit == suit:
                ans.append(_cards[j])
        if len(ans) >= 5:
            return ans[:5]
  
    return None

def search_four_of_a_kind(cards):
    '''
    cards: sorted cards by rank high to low
    '''
    for i in range(len(cards)-4):
        rank = cards[i].rank
        j = 1
        while j < 5 and cards[i+j].rank == rank:
            j += 1
        if j == 5:
            return cards[i:i+5]
        
    return None

def search_full_house(cards):
    '''
    cards: sorted cards by rank high to low
    '''
    rank_count = Counter([card.rank for card in cards])
    ranks = sorted(rank_count.keys(), reverse = True)
    
    hand = []
    for rank in ranks:
        if rank_count[rank] == 3:
            for card in cards:
                if card.rank == rank:
                    hand.append(card)
            break
    
    if not hand:
        return None
    
    for rank in ranks:
        if rank_count[rank] >= 2 and rank != hand[0].rank:
            for card in cards:
                if card.rank == rank:
                    hand.append(card)
            break
    
    if len(hand) >= 5:
        return hand[:5]
    
    return None

def search_flush(cards):
    '''
    cards: sorted cards by rank high to low
    '''
    suit_count = Counter([card.suit for card in cards])
    for suit in suit_count:
        if suit_count[suit] >= 5:
            hand = []
            for card in cards:
                if card.suit == suit:
                    hand.append(card)
            return hand[:5]
    
    return None

def search_straight(cards):
    # cover low straight flush possibility
    _cards = [card for card in cards]
    for card in cards:
        if card.rank < 14:
            break
        _cards.append(Card(1, card.suit))
    
    for i in range(len(_cards)-4):
        ans = [_cards[i]]
        for j in range(i+1,len(_cards)):
            if _cards[j].rank < ans[-1].rank - 1:
                break
            if _cards[j].rank == ans[-1].rank - 1:
                ans.append(_cards[j])
        if len(ans) >= 5:
            return ans[:5]

    return None

def search_three_of_a_kind(cards):
    '''
    cards: sorted cards by rank high to low
    '''
    rank_count = Counter([card.rank for card in cards])
    ranks = sorted(rank_count.keys(), reverse = True)
    
    hand = []
    for rank in ranks:
        if rank_count[rank] == 3:
            for card in cards:
                if card.rank == rank:
                    hand.append(card)
            break
    
    if not hand:
        return None
    
    for card in cards:
        if card.rank != hand[0].rank:
            hand.append(card)
            
    return hand[:5]

def search_two_pairs(cards):
    '''
    cards: sorted cards by rank high to low
    '''
    rank_count = Counter([card.rank for card in cards])
    ranks = sorted(rank_count.keys(), reverse = True)
    
    pair_ranks = []
    for rank in ranks:
        if rank_count[rank] == 2:
            pair_ranks.append(rank)
    
    if len(pair_ranks) < 2:
        return None
    
    hand = [card for card in cards if card.rank == pair_ranks[0]] \
        + [card for card in cards if card.rank == pair_ranks[1]]
    
    for card in cards:
        if card.rank not in pair_ranks:
            hand.append(card)
            return hand
        
def search_one_pair(cards):
    '''
    cards: sorted cards by rank high to low
    '''
    rank_count = Counter([card.rank for card in cards])
    pair_rank = None
    for rank in rank_count:
        if rank_count[rank] == 2:
            pair_rank = rank
            break
    
    if not pair_rank:
        return None
    
    hand = [card for card in cards if card.rank == pair_rank]
    for card in cards:
        if card.rank != pair_rank:
            hand.append(card)
    
    return hand[:5]

def update_best_hand(player, common_cards):
    '''
    find highest hand in cards
    update player.best_hand, player.score
    '''
    cards = player.cards + common_cards
    #cards = sorted(cards, key=lambda card: card.rank, reverse = True)
    
    player.best_hand_type, player.best_hand = find_best_hand(cards)


def find_best_hand(cards):
    '''
    cards: sorted cards
    return best_hand, best_hand_type
    '''
    
    cards.sort(key=lambda c:c.rank, reverse = True)
    
    if len(cards) == 2:
        # TO DO
        return
    else:
        # find highest 5 cards out of all cards
        ans = search_straight_flush(cards)
        if ans:
            return HANDS[0], ans
        
        ans = search_four_of_a_kind(cards)
        if ans:
            return HANDS[1], ans
        
        ans = search_full_house(cards)
        if ans:
            return HANDS[2], ans
        
        ans = search_flush(cards)
        if ans:
            return HANDS[3], ans
        
        ans = search_straight(cards)
        if ans:
            return HANDS[4], ans
        
        ans = search_three_of_a_kind(cards)
        if ans:
            return HANDS[5], ans
        
        ans = search_two_pairs(cards)
        if ans:
            return HANDS[6], ans
        
        ans = search_one_pair(cards)
        if ans:
            return HANDS[7], ans
        
        return HANDS[8], cards[:5]

def calculate_score(best_hand_type, best_hand):
    '''
    update player.score based on best_hand_type and best_hand
    use base 13 numbering
    6 (type), 5 , 4, 3, 2, 1
    '''
    
    digits = '0123456789TJQKA'
    
    #score = 0
    letter_score = ''
    
    i = 0
    #power = 6
    while HANDS[i] != best_hand_type:
        i += 1
    
    #score += (len(HANDS)-i)*(13**power)
    #power -= 1
    letter_score = str(len(HANDS)-i)

    cards = best_hand
    for i in range(5):
        #score += (cards[i].rank)*(13**power)
        #power -= 1
        letter_score = digits[cards[i].rank] + letter_score
    
    # handles low straight flush and low straight
    if sorted([card.rank for card in cards]) == [2, 3, 4, 5, 14]:
        if all(card.suit == cards[0].suit for card in cards):
            letter_score = '912345'
        else:
            letter_score = '512345'
    
    return letter_score

def distribute(ranked_players):
    '''
    ranked_players: list of players ranked by their score
    distribute pots to players
    Returns None
    '''
    score_player = defaultdict(list)
    for player in ranked_players:
        score_player[player.score].append(player)
    
    bets = sorted(list(set([p.money_in_pot for p in ranked_players])))
    bets = [0] + bets
    
    bet_player = {bet:[] for bet in bets}
    
    for player in ranked_players:
        for b in bets:
            if player.money_in_pot >= b:
                bet_player[b].append(player)
    
    for b in bet_player:
        bet_player[b].sort(key=lambda p:p.score, reverse=True)

    # iterate each bet level, find the unfolded player(s) w. the highest score
    for i in range(1, len(bets)):
        b = bets[i]
        winners = []
        for p in bet_player[b]:
            if p.folded:
                continue
            if not winners:
                winners.append(p)
            elif p.score == winners[0].score:
                winners.append(p)
            else:
                break
        
        if not winners:
            continue
        
        pot = 0
        incre = bets[i] - bets[i-1]
        for p in bet_player[b]:
            pot += min(p.money_in_pot, incre)
            p.money_in_pot -= min(p.money_in_pot, incre)
        
        mod = pot % len(winners)
        for i in range(mod):
            winners[i].money += 1
        
        pot -= mod
        for p in winners:
            p.money += pot // len(winners)
        
    # iterate through players. Each gets back any outstanding betted money
    # this covers folded player who has higher bet than all-in player, 
    # and last un-called raised player
    for p in ranked_players:
        if p.money_in_pot > 0:
            p.money += p.money_in_pot
            p.money_in_pot = 0
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            