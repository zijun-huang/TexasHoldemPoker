# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 19:22:21 2020

@author: Zijun Huang
"""


def bet(player, max_bet):
        '''
        returns bet, amount
        '''
        while True:
            try:
                if max_bet == player.money_in_pot:
                    if player.money > 0:
                        options = ['fold', 'check', 'bet']
                    else:
                        options = ['fold', 'check']
                else:
                    if player.money > max_bet - player.money_in_pot:
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
            return bet, min(player.money, max_bet - player.money_in_pot)
        
        if bet == 'bet' or 'raise':
            while True:
                try:
                    minBet = max_bet-player.money_in_pot +1
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