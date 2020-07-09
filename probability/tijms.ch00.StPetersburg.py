#!/usr/bin/env python3
"""
In 1738 Daniel Bernoulli (1700– 1782), one of the many mathematicians of the famous Bernoulli family, presented before the 
Imperial Academy of Sciences in St. Petersburg a classic paper on probability, in which he discussed the following problem. 

In a certain casino game, a fair coin is tossed successively until the moment that heads appears for the first time. 
The casino payoff is two dollars if heads turns up in the first toss, four dollars if heads turns up for the first time in the second toss, etc. 
In general, the payoff is 2n dollars if heads turns up for the first time in the nth toss. 
Thus, with each additional toss the payoff of the casino is doubled. 

What amount must the casino require the player to stake such that, over the long term, the game will not be a losing endeavor for the casino? 
To answer this question, we need to calculate the expected value of the casino payoff for a single repetition of the game. 
The probability of getting heads in the first toss is , the probability of getting tails in the first toss and heads in 
the second toss is × , etc., and the probability of getting tails in the first n – 1 tosses and heads in the nth toss is 

    1/2 $2 + 1/4 $4 + 1/8 $8 + ... + 1/n $(2**n) + ...

The expected value of the casino payoff for a single repetition of the game is thus equal to In this infinite series, 
a figure equal to $ 1 is added to the sum each time. In this way, the sum exceeds every conceivable large value and 
mathematicians would say that the sum of the infinite series is infinitely large. 
The expected value of the casino payoff for a single repetition of the game is thus an infinitely large dollar amount.

The problem does become more realistic when the following modification is made to the game. 
The casino can only pay out up to a limited amount. To simplify the matter, let’s assume that the maximum payoff is a given multiple of 2. 
Let the maximum casino payoff per game be equal to 2M dollars for some given integer M (e.g., M = 15 would correspond with a maximum payoff of $ 32,768). 
In every repetition of the game a fair coin is tossed until either heads appears for the first time or M tosses are executed without heads appearing. 
The casino pays the player 2k dollars when heads appears for the first time in the kth toss and pays nothing if tails is tossed M times in a row. 
What must the player’s minimum stake be such that the game will not be a loss for the casino over the long term? 
The same reasoning we used before says that the expected value of the casino payoff for a single execution of the game is equal to

    1/2 $2 + 1/4 $4 + 1/8 $8 + ... + 1/M $(2**M) = $M

Tijms, Henk (2012-06-14). Understanding Probability (p. 42). 
Cambridge University Press
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt


def simulate(M, verbose):
    """(int, bool): int
    """

    dice_throw  = np.random.randint(0,2,M)
    dice_string = ''.join(str(x) for x in dice_throw)       # represents 1 as Tail and 0 as Heads. 
    total_tails = np.count_nonzero(dice_throw)
    if (total_tails >= M):
        # not a single 0 or heads, maximum payoff applies
        k = M - 1
    else:
        k = np.argmin(dice_throw)                           # this is the first appearance of Heads
    pay = 2 ** (k + 1)                                      # amount to pay
    if verbose:
        print('M={} {} First_Head={} pay ${}'.format(M, dice_string, (k+1), pay))
    
    return pay


def main():
    # Get command-line arguments
    parser = argparse.ArgumentParser(
        description='simulate the Bernoulli St Petersburg Problem')
    parser.add_argument('--M', default=20, type=int, metavar='int',
                        help='maximum payoff as in 2**M')
    parser.add_argument('--trials', default=10000, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='display the results of each trial')
    args = parser.parse_args()

    print('Simulating St Petersburg for Maximum Payoff {} (${:,}) {:,} trials...'.format(args.M, 2 ** args.M, args.trials))

    # Carry out the trials
    total_paid   = 0
    results      = np.empty(0)
    max_pay      = 0
    for i in range(args.trials):
        # First, do a trial where the contestant never switches.
        won          = simulate(args.M, verbose=args.verbose)
        max_pay      = max(won,max_pay)
        total_paid  += won
        results      = np.append(results,total_paid/(i+1))

    print('M {} trials {}  Max Paid={} min/max {:.2f}/{:.2f} final value {:.4f} '.format(args.M, args.trials, max_pay, np.amin(results), np.amax(results), results[-1] ))
    x = np.arange(0,args.trials) # Generate x-axis values
    plt.figure(figsize=(10, 5), dpi=240)
    plt.plot(x,results,'r')
    fig = plt.gcf()
    ax  = plt.gca()
    plt.title('St Petersburg Simulation', fontname='Times New Roman',fontweight='bold')
    plt.xlabel('Trial')
    plt.ylabel('average payoff')
    plt.axhline(y=args.M, xmin=0, xmax=args.trials, hold=None, c='blue',linewidth=0.5, ls='dashed')
    plt.text(args.trials/2, args.M/2, 'Max pay {:,} ({:.2f}/{:.2f})'.format(max_pay,np.amin(results), np.amax(results)))
    plt.show()
    
    #fig.set_size_inches(10,5)
    fig.savefig('tijms.ch00.StPetersburg.png')

if __name__ == '__main__':
    main()