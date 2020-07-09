#!/usr/bin/env python3
"""
In casino games, the gambler often has the intention to play the game repeatedly until he either increases 
his bankroll to a predetermined level or goes broke. Imagine a gambler who starts with an initial bankroll 
of a dollars and then on each successive gamble either wins one dollar or loses one dollar with 
probabilities p and q = 1 – p respectively. The gambler stops playing after having raised his bankroll 
to a + b dollars or running out of money, whichever happens first. Here a and b are positive integers. 
What is the gambler’s probability of reaching his desired goal before going broke? 
This is commonly known as the gambler’s ruin problem. The progress of the gambler’s bankroll forms a random 
walk in which there is a probability p of moving one unit in the positive direction and a probability q of 
moving one unit in the other direction. The random walk eventually reaches one of the absorbing states 
0 or a + b and then stops.

Tijms, Henk (2012-06-14). Understanding Probability (p. 93). Cambridge University Press. Kindle Edition. 
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys


def simulate(p, a, b, x, verbose):
    """(real, int, int, int, bool): int
        p is the probability of moving to the right, or winning, and q = 1 - p is of losing
        a is the initial bankroll, or starting point in the X coordinate for a random walk
        b + a is the desired exit winning bankroll, or the rightmost absorbing state
        x is the leftmost exit losing bankroll, typically 0, that signals end of game
        
        n is number of moves needed to reach a + b or x
        q is bankroll at end
        k is amount of times moves returned to a
        v is amount of stations between x and a + b that have never been visited
        m is maximum bankroll
        Returns [n, q, k , v]
    """

    segment     = np.zeros(shape=(1+a+b-x),dtype=np.int16)
    segment[a]  = 1                                                 # visited from start...
    n           = 0                                                 # initialize total movements
    k           = 0                                                 # initialize return to a to zero
    q           = a                                                 # bankroll to start
    m           = a                                                 # max wins
    z           = a                                                 # min wins
    history     = [q]
    
    while q > x and q < a + b:
        move         = np.random.choice([ -1, 1],p=[1 - p, p])       # first move, either left or right...
        q            += move
        history.append(q)
        if q > m:    m = q
        if q < z:    z = q
        segment[q-x] += 1
        n            += 1
        if q == a: k += 1
        if verbose: print('{} '.format(q),end='');
        if verbose and n % 5 == 0 : 
            print(' *** ',end='');
            sys.stdout.flush()
    
    v  = np.sum((segment == 0))
    if verbose: print('exit with n,q,k,v,m,z {},{},{},{},{}'.format(n,q,k,v,m,z))
    return [n,q,k,v,m,z,history]


def main():
    np.random.seed()
    # Get command-line arguments
    parser = argparse.ArgumentParser(description='simulate the Gamblers Ruin Random Walk Problem')
    parser.add_argument('--p', default=0.5, type=float, metavar='float',
                        help='winning probability')
    parser.add_argument('--a', default=10, type=int, metavar='int',
                        help='initial bankroll')
    parser.add_argument('--x', default=0, type=int, metavar='int',
                        help='exit level of money in bankroll')
    parser.add_argument('--b', default=5, type=int, metavar='int',
                        help='desired pot')
    parser.add_argument('--trials', default=10, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--xmx', default=10000, type=int, metavar='int',
                        help='plot coordinate max X')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='display the results of each trial')
    args = parser.parse_args()

    print('Simulating Gamblers Ruin starting with {} and desire to win {}. Winning prob={:.2f} exit game level {} --- {:,} trials...\n'.format(args.a, args.b, args.p, args.x, args.trials))
    xmx = args.xmx
    x = np.arange(0,xmx) # Generate x-axis values
    plt.figure(figsize=(10, 5), dpi=240)
    plt.title('Gamblers Ruin', fontname='Times New Roman',fontweight='bold')
    plt.xlabel('games')
    plt.ylabel('Bankroll')
    plt.axhline(y=args.a, xmin=0, xmax=xmx, c='green',linewidth=0.5, ls='dashed')
    plt.axhline(y=args.a+args.b, xmin=0, xmax=xmx, c='blue',linewidth=0.5, ls='dashed')

    plt.text(10, args.x+5 , 'p={:.2f} Initial={} Win={}'.format(args.p,args.a,args.a+args.b))

    # Carry out the trials
    for i in range(args.trials):
        (n, q, k, v, m, z, y) = simulate(args.p, args.a, args.b, args.x, args.verbose)
        if q == args.x: 
            print('BROKEN ',end='')
        else:
            print('WINNER ',end='')
        print('Total games played: {:,}; Final bankroll: {} ({} times going back to original amount; money max: {:,} min: {:,}; never reached {})\n'.format(n,q,k,m,z,v))
        y.extend([q] * xmx)
        del y[xmx:]
        plt.plot(x, y, linewidth=0.5)
        
    print('Done\n')

    plt.show()
    fig = plt.gcf()
    ax  = plt.gca()

    #fig.set_size_inches(10,5)
    fig.savefig('tijms.ch00.GamblersRuin.png')



if __name__ == '__main__':
    main()
