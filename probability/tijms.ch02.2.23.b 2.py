#!/usr/bin/env python3

"""
    Exercise 2.18 
    What is the probability that in a thoroughly shuffled deck of 52 cards no two adjacent cards are of the same rank? 
    
    Tijms, Henk (2012-06-14). Understanding Probability (p. 68). Cambridge University Press. Kindle Edition. 
"""


import argparse
import numpy as np
import matplotlib.pyplot as plt

import random
import functools


def simulate_wordpermutation(verbose, word):
    """(string [,bool]): bool
    convert to list, permutate/shuffle, check if two adjacent letters are there, return True or False
    """

    letter_list = list(word)
    random.shuffle(letter_list)
    adjacent = functools.reduce(lambda x, y: 0 if x == y or x == 0 else y, letter_list)
    if verbose: print('Word {} Shuffle {} adjacents {}'.format(word, ''.join(letter_list), adjacent == 0))
    return adjacent == 0



def main():
    # Get command-line arguments
    parser = argparse.ArgumentParser(description='Tijms, Henk (2012-06-14). Understanding Probability Exercise 2.18')
    parser.add_argument('--verbose',    default=False,          action='store_true',            help='display the results of each trial')
    parser.add_argument('--trials',     default=10000,          type=int, metavar='int',        help='number of trials to perform')
    parser.add_argument('--word',       default='1234567890JQK1234567890JQK1234567890JQK1234567890JQK',   type=str, metavar='str',        help='word to use for permutations')
    args = parser.parse_args()
    

    tot_count   = 0
    print('starting...')
    for i in range(args.trials):
        if i % 50   == 0 and i != 0: print('-+-',end='');
        if i % 2000 == 0 and i != 0: print('***2000***');
        # First, do a trial where the contestant never switches.
        adjacent    = simulate_wordpermutation(verbose=args.verbose, word=args.word)
        if not adjacent: tot_count   += 1 
    # now we are done with the trials, compute the vectors
    print('-+-\nDone\n')
    avg_count   = tot_count / args.trials
    print('Word {} [{:,} trials] --- Probability of not any two adjacent alike {:,.4f} or {:.2f}%'.format(args.word, args.trials, avg_count, avg_count * 100)) 
    
    

if __name__ == '__main__':
    main()

