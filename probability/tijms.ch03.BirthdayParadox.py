#!/usr/bin/env python3
"""
The birthday problem is very well known in the field of probability theory. It raises the following interesting questions: 
What is the probability that, in a group of randomly chosen people, at least two of them will have been born on the same day of the year? 
How many people are needed to ensure a probability greater than 0.5?

In the almost-birthday problem, we undertake the task of determining the probability of two or more people in a randomly assembled group
of n people having their birthdays within r days of each other. Denoting this probability by pn( r), it is given by 
    
    pn(r) = 1 - (365 -1 - nr)! / 365^(n-1) (365 - (r+1)n)!
    
The proof of this formula is rather tricky and can be found in J.I. Nauss, “An Extension of the Birthday Problem,” 
The American Statistician 22 (1968): 27– 29. Although the almost-birthday problem is far more complicated than the ordinary birthday 
problem when it comes to theoretical analysis, this is not the case when it comes to computer simulation.

Tijms, Henk (2012-06-14). Understanding Probability (p. 76). Cambridge University Press. Kindle Edition. 

"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys


def simulate(N, D, r, verbose):
    """(int, int, int, bool): int
        Where N is number of people (or things); D is number of days (365 for a year); and r is the days between birthdays, 0 for same day
        Returns True if not two people have randomly assigned birthdays in 1..D with r or less difference
    """

    assign_birthdays = np.random.randint(1,D,N)             # create array with N elements chosen randomly in 1..D
    sorted_birthdays = np.sort(assign_birthdays)            # sort elements to find matches  
    if verbose: print('{}'.format(sorted_birthdays))
    i = 0
    while i < N - 1:
        if verbose: print('iter {:03d} {} {}'.format(i, sorted_birthdays[i], sorted_birthdays[i+1] ))
        if sorted_birthdays[i+1] - sorted_birthdays[i] <= r: return False
        i += 1
    if verbose: print('end iter {}'.format(i))   
    return True


def main():
    # Get command-line arguments
    parser = argparse.ArgumentParser(
        description='simulate the Birthday Paradox Problem')
    parser.add_argument('--N', default=23, type=int, metavar='int',
                        help='number of guests')
    parser.add_argument('--D', default=365, type=int, metavar='int',
                        help='number of days, default 365')
    parser.add_argument('--r', default=0, type=int, metavar='int',
                        help='number of days between birthdays, default is 0 (same day)')
    parser.add_argument('--trials', default=10000, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='display the results of each trial')
    args = parser.parse_args()

    print('Simulating Birthday Paradox for {} people with {} days and {} days apart {:,} trials...'.format(args.N, args.D, args.r, args.trials))

    # Carry out the trials
    total_match = 0
    for i in range(args.trials):
        if i % 50   == 0 and i != 0: print('-+-',end='');
        if i % 2000 == 0 and i != 0: print('***2000***');
        sys.stdout.flush()
        nottwo   = simulate(args.N, args.D, args.r, verbose=args.verbose)
        if args.verbose: print('simulate {}'.format(nottwo)) 
        if nottwo == True:
            total_match += 1 
            if args.verbose: print('total_match {}'.format(total_match))
    print('-+-\nDone\n')

    print('Probability of not two birthdays {} days apart ({:,} people and {:,} days) {:.6f}  {:.2f}% [at least two {:.2f}%]'.format(args.r, args.N, args.D, total_match / args.trials, total_match / args.trials * 100, (1 - total_match / args.trials) * 100))
    #pnr = lambda D, N, r: (1 - np.math.factorial(D - 1 - N * r) / (np.power(D, N - 1) * np.math.factorial(D - N * (r + 1))))
    #print ('Theoretical formula: {:.6f} '.format(pnr(args.D,args.N,args.r))) 

if __name__ == '__main__':
    main()