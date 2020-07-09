#!/usr/bin/env python3

"""
    Exercise 2.18 
    The popular dice game “drop dead” goes as follows. 
    Each player in turn rolls the five dice and scores when none of the dice thrown show a 2 or a 5. 
    If a 2 or a 5 are not thrown, then the player scores the total of the numbers rolled. 
    If a 2 or 5 is thrown the player scores nothing and puts aside all the dice showing a 2 or 5. 
    These dice are dead and the player continues rolling without them, each time scoring only when no 2s or 5s are 
    rolled and putting aside any dice showing a 2 or a 5. The player’s turn ends when all the dice are eliminated. 
    Use simulation to find the expected length and expected total score of a player’s turn. 
    Also, simulate the probability that the total score will be more than k points, 
    where k = 0, 5, 10, 15, 25, 35, and 50.

    Tijms, Henk (2012-06-14). Understanding Probability (p. 68). Cambridge University Press. Kindle Edition. 
"""


import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.stdout.flush()


def simulate_dropdead(verbose):
    """(bool [,bool]): [bool, bool]
    Carry out simulation. Find A, B, C randomly in (-q,q)
    """
    # throw 5 dice (1 to 6) and record
    count = 0
    dice  = 5
    score = 0
    while True:
        throw   = np.random.randint(low=1,high=7,size=dice)
        count   += 1
        bad     = np.count_nonzero(throw == 2) + np.count_nonzero(throw == 5)
        if  bad == 0: score   += np.sum(throw)
        dice    -= bad
        if verbose: print('Throw {} dice {} {} bad {} score {}'.format(count, dice, throw, bad, score))
        if dice == 0: break
    if verbose: print('*** count {} score {}'.format(count, score))
    return [count, score]



def main():
    # Get command-line arguments
    parser = argparse.ArgumentParser(
        description='simulate the Newspaper arrival problem')
    parser.add_argument('--trials', default=10000, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='display the results of each trial')
    args = parser.parse_args()
    

    k  = [0, 5, 10, 15, 25, 35, 50]
    nk = [0, 0,  0,  0,  0,  0,  0]
    np_k  = np.array(k)
    np_nk = np.array(nk)

    tot_count   = 0
    tot_score   = 0
    max_score   = 0
    print('starting...')
    for i in range(args.trials):
        if i % 50   == 0 and i != 0: print('-+-',end='');
        if i % 2000 == 0 and i != 0: print('***2000***');
        # First, do a trial where the contestant never switches.
        (count, score) = simulate_dropdead(verbose=args.verbose)
        if score > max_score: max_score = score
        tot_count += count
        tot_score += score
        i = 0
        while True:
            if score > np_k[i]: np_nk[i] += 1
            i += 1
            if i >= np_k.size: break
        if args.verbose: print('--- count {} score {} {} {}'.format(count, score, np_k, np_nk))
    # now we are done with the trials, compute the vectors
    print('-+-\nDone\n')
    p_nk        = np_nk / args.trials * 100
    avg_count   = tot_count / args.trials
    avg_score   = tot_score / args.trials
    print('MAX score {} [{:,} trials] --- AVG count {:,.2f}  score {:,.2f}  '.format(max_score, args.trials, avg_count, avg_score)) 
    print('Probability distribution')
    i = 0 
    while True:
        print('Probability[score > {:02d}] is {:,.2f}%'.format(np_k[i], p_nk[i])) 
        i += 1
        if i >= np_k.size: break
    
    

if __name__ == '__main__':
    main()

