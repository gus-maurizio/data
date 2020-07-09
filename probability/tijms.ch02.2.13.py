#!/usr/bin/env python3

"""
    Exercise 2.13 Cuadratic Equation Ax**2+Bx+C=0
    Probability it has real roots (B**2-$AC >=0) when A, B, C are selected randomly
    in interval (-q,q) or integers in -q..q
    Solve for q = 1; 10; 100; 1000; 10000
"""


import argparse
import numpy as np
import matplotlib.pyplot as plt



def simulate_AX2BXC_real(q, verbose):
    """(real, bool)
    Carry out simulation. Find A, B, C randomly in (-q,q)
    """
    A, B, C = np.random.random(3) * 2 * q - q
    discriminator = B ** 2 - 4 * A * C
    real_root = ( discriminator >= 0)
    if verbose:
        print('REAL q={} A {} B {} C {} discriminator {}  {}'.format(q,A,B,C,discriminator,real_root))
    return real_root

def simulate_AX2BXC_int(q, verbose):
    """(real, bool)
    Carry out simulation. Find A, B, C randomly in (-Q,Q)
    """
    A, B, C = np.random.randint(low=-q, high=q+1, size=3)
    discriminator = B ** 2 - 4 * A * C
    real_root = ( discriminator >= 0)
    if verbose:
        print('INT  q={} A {} B {} C {} discriminator {}  {}'.format(q,A,B,C,discriminator,real_root))
    return real_root


def main():
    # Get command-line arguments
    parser = argparse.ArgumentParser(
        description='simulate the Newspaper arrival problem')
    parser.add_argument('--q', default=1, type=int, metavar='int',
                        help='Interval q (-q,q)')
    parser.add_argument('--trials', default=10000, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--real', default=True, action='store_true',
                        help='use (-q,q) as real numbers, otherwise use -Q..Q as Integers')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='display the results of each trial')
    args = parser.parse_args()
    

    real_roots = 0
    intg_roots = 0
    for i in range(args.trials):
        # First, do a trial where the contestant never switches.
        real_root = simulate_AX2BXC_real(args.q, verbose=args.verbose)
        if real_root: real_roots += 1
        real_root = simulate_AX2BXC_int(args.q, verbose=args.verbose)
        if real_root: intg_roots += 1
    
    print('Q={0} REAL has real roots  {1:,} times out of {2:,} ({3:.2f}% of the time)'.format(
            args.q, real_roots, args.trials, (real_roots / args.trials * 100) ))
    print('Q={0} INTG has real roots  {1:,} times out of {2:,} ({3:.2f}% of the time)'.format(
            args.q, intg_roots, args.trials, (intg_roots / args.trials * 100) ))



if __name__ == '__main__':
    main()

