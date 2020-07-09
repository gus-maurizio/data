#!/usr/bin/env python3
"""
Random walk with probabilities p and q = 1 – p respectively. p to move to the right.

Tijms, Henk (2012-06-14). Understanding Probability (p. 93). Cambridge University Press. Kindle Edition. 
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys


def simulate(p, n, verbose):
    """(real, int, bool): int
        p is the probability of moving to the right, or winning, and q = 1 - p is of losing
        n is the amount of steps to take
        
        q is final position
        k is amount of times moves returned to a
        m is maximum distance
        z is minimum distance
        t is list of positions
        avg is average displacement
        std is std deviation
        Returns [q, k , m, z, t]
    """

    k           = 0                                                 # initialize return to a to zero
    q           = 0                                                 # bankroll to start
    m           = 0                                                 # max wins
    z           = 0                                                 # min wins
    
    i           = 0
    t           = [0]
    while i < n:
        move         = np.random.choice([ -1, 1],p=[1 - p, p])       # first move, either left or right...
        q            += move
        t.append(q)
        if q > m:   m = q
        if q < z:   z = q
        if q == 0:  k += 1
        i   +=1
        if verbose: print('{} '.format(q),end='');
        if verbose and n % 100 == 0 : 
            print(' ***');
            sys.stdout.flush()
    
    if verbose: print('exit with q,k,m,z {},{},{},{} {}'.format(q,k,m,z,t))
    return [q,k,m,z,t]


def main():
    np.random.seed()
    # Get command-line arguments
    parser = argparse.ArgumentParser(description='simulate the Gamblers Ruin Random Walk Problem')
    parser.add_argument('--p', default=0.5, type=float, metavar='float',
                        help='right move probability')
    parser.add_argument('--n', default=10000, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--trials', default=10, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='display the results of each trial')
    args = parser.parse_args()

    print('Simulating Random Walk with right prob={:.2f} and {:,} moves --- {:,} trials...\n'.format(args.p, args.n, args.trials))
    xmx = args.n + 1
    x = np.arange(0,xmx) # Generate x-axis values
    plt.figure(figsize=(10, 5), dpi=240)
    plt.title('Random Walk with p={:.4f}'.format(args.p), fontname='Times New Roman',fontweight='bold')
    plt.xlabel('moves')
    plt.ylabel('position')
    plt.axhline(y=0, xmin=0, xmax=xmx, c='grey',linewidth=0.5, ls='dashed')

    # Carry out the trials
    for i in range(args.trials):
        (q, k, m, z, t) = simulate(args.p, args.n, args.verbose)
        print('Final position: {:,} ({:,} times going back to origin; max: {:,} min: {:,})'.format(q,k,m,z))
        plt.plot(x, t, linewidth=0.5, label='Trial {} ({:,}/{:,}) - end: {:,}'.format(i+1,m,z,q))
        
    print('Done\n')

    plt.legend(fontsize=6, shadow=True)
    plt.show()
    fig = plt.gcf()
    ax  = plt.gca()

    #fig.set_size_inches(10,5)
    fig.savefig('tijms.ch00.RandomWalk.png')



if __name__ == '__main__':
    main()
