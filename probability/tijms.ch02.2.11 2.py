#!/usr/bin/env python3

"""
    Exercise 2.11 Newspaper arrival between 6:30-7:30. Mr Jones leaves between 7:00-8:00.
    What is the probability that Mr Jones gets the Newspaper to work?
"""

import  argparse,   \
        random,     \
        time

from datetime import datetime as dtt


def simulate(narr, nend, wstart, wend, verbose):
    """(datetime, datetime, datetime, datetime, bool)
    Carry out simulation. Newspaper will be randomly delivered between narr and nend,
    person leaves random between wstart and wend
    Returns a Boolean value telling whether the person received the newspaper before leaving.
    """
    ndelta = nend - narr
    wdelta = wend - wstart
    if wstart >= nend:
        print('Subject leaves after late newspaper arrival time.')
        return false
    
    newspaper   = random.random() * ndelta
    person      = random.random() * wdelta
    
    take_newspaper = ( (narr + newspaper) <= (wstart + person))
    
    if verbose:
        print('Newspaper arrives {} person leaves {} {}'.format((narr + newspaper), (wstart + person), take_newspaper))
    
    return take_newspaper


def main():
    # Get command-line arguments
    parser = argparse.ArgumentParser(
        description='simulate the Newspaper arrival problem')
    parser.add_argument('--newsfrom', default='06:30', type=str, metavar='str',
                        help='Newspaper arrival time in HH:MM')
    parser.add_argument('--newsto', default='07:30', type=str, metavar='str',
                        help='Newspaper cutoff time in HH:MM')
    parser.add_argument('--workfrom', default='07:00', type=str, metavar='str',
                        help='Work Departure early time in HH:MM')
    parser.add_argument('--workto', default='08:00', type=str, metavar='str',
                        help='Work Departure late time in HH:MM')
    parser.add_argument('--trials', default=1000, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='display the results of each trial')
    args = parser.parse_args()
    
    narr_time = dtt.strptime(args.newsfrom, "%H:%M")
    nend_time = dtt.strptime(args.newsto, "%H:%M")
    
    wfrom_time = dtt.strptime(args.workfrom, "%H:%M")
    wto_time   = dtt.strptime(args.workto, "%H:%M")
    
    ndelta = nend_time - narr_time
    wdelta = wto_time - wfrom_time
    
    print('Newspaper Arrival Time from {} to {} for {}...'.format(narr_time, nend_time,ndelta))
    print('Work Departure Time from {} to {} for {}...'.format(wfrom_time, wto_time,wdelta))
    
    if wfrom_time >= nend_time:
        print('Subject leaves after late newspaper arrival time.')
        quit()
    
    overlap = nend_time - wfrom_time    
    print('Overlap is {}...'.format(overlap))
    print('Simulating {} trials...'.format(args.trials))
    
    simulate(narr_time, nend_time, wfrom_time, wto_time, verbose=args.verbose)
    # Carry out the trials
    times_taken = 0
    for i in range(args.trials):
        # First, do a trial where the contestant never switches.
        taken = simulate(narr_time, nend_time, wfrom_time, wto_time, verbose=args.verbose)
        if taken:
            times_taken += 1
    
    print('Newspaper taken {0:,} times out of {1:,} ({2:.4}% of the time)'.format(
            times_taken, args.trials, (times_taken / args.trials * 100) ))



if __name__ == '__main__':
    main()

