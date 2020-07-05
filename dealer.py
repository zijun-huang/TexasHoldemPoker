# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 10:03:57 2020

@author: Zijun Huang
"""

from collections import Counter, defaultdict

HANDS = ["Straight Flush", "Four of a Kind", "Full House", "Flush", 
         "Straight", "Three of a Kind","Two Pairs", "One Pair", "No Pair"]


def search_straight_flush(cards):
    '''
    cards: sorted cards by rank high to low
    '''
    for i in range(len(cards)-4):
        rank, suit = cards[i].rank, cards[i].suit
        j = 1
        while j < 5 and cards[i+j].rank == rank-j and cards[i+j].suit == suit:
            j += 1
        if j == 5:
            return cards[i:i+5]
    
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
    for i in range(len(cards)-4):
        rank = cards[i].rank
        j = 1
        while j < 5 and cards[i+j] == rank-j:
            j += 1
        if j == 5:
            return cards[i:i+5]
        
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
    
def find_highest_hand(player, common_cards):
    '''
    find highest hand in cards
    update player.highest_hand, player.score
    '''
    cards = player.cards + common_cards
    cards = sorted(cards, key=lambda card: card.rank, reverse = True)
    
    if len(cards) == 2:
        # TO DO
        return
    else:
        # find highest 5 cards out of all cards
        ans = search_straight_flush(cards)
        if ans:
            player.highest_hand = ans
            player.highest_hand_type = HANDS[0]
            return
        
        ans = search_four_of_a_kind(cards)
        if ans:
            player.highest_hand = ans
            player.highest_hand_type = HANDS[1]
            return
        
        ans = search_full_house(cards)
        if ans:
            player.highest_hand = ans
            player.highest_hand_type = HANDS[2]
            return
        
        ans = search_flush(cards)
        if ans:
            player.highest_hand = ans
            player.highest_hand_type = HANDS[3]
            return
        
        ans = search_straight(cards)
        if ans:
            player.highest_hand = ans
            player.highest_hand_type = HANDS[4]
            return
        
        ans = search_three_of_a_kind(cards)
        if ans:
            player.highest_hand = ans
            player.highest_hand_type = HANDS[5]
            return
        
        ans = search_two_pairs(cards)
        if ans:
            player.highest_hand = ans
            player.highest_hand_type = HANDS[6]
            return
        
        ans = search_one_pair(cards)
        if ans:
            player.highest_hand = ans
            player.highest_hand_type = HANDS[7]
            return
        
        player.highest_hand = cards[:5]
        player.highest_hand_type = HANDS[8]
        
        return

def calculate_score(player):
    '''
    update player.score based on highest_hand_type and highest_hand
    use base 13 numbering
    6 (type), 5 , 4, 3, 2, 1
    '''
    score = 0
    
    i = 0
    power = 6
    while HANDS[i] != player.highest_hand_type:
        i += 1
    
    score += (len(HANDS)-i)*(13**power)
    power -= 1   

    cards = player.highest_hand
    for i in range(5):
        score += (cards[i].rank)*(13**power)
        power -= 1
    
    player.score = score

def distribute(ranked_players):
    '''
    ranked_players: list of players ranked by their score
    distribute pots to players
    Returns None
    '''
    score_player = defaultdict(list)
    for player in ranked_players:
        score_player[player.score].append(player)
    
    bet_player = defaultdict(list)
    for player in ranked_players:
        bet_player[player.moneyBetted].append(player)
    
    bets = sorted(bet_player.keys())
    
    # TO DO
    
    