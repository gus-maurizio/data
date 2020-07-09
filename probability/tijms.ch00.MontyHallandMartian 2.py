#!/usr/bin/env python3

"""Simulate the Monty Hall problem.
   Before opening door, add a new contestant -Martian- that can choose randomly between the two closed doors

"""

import  argparse, \
        random

def simulate(num_doors, switch, verbose):
    """(int, bool [,bool]): [bool, bool]

    Carry out the game for one contestant.  If 'switch' is True,
    the contestant will switch their chosen door when offered the chance.
    Returns a Boolean value telling whether the simulated contestant won.
    The Martian will make a choice between the last two closed doors, independent
    of the contestant choice, at random.
    """
    if verbose:
        print('\n** switch {}'.format(switch))

    goat    = 'G'
    car     = 'C'
    # Doors are numbered from 0 up to num_doors-1 (inclusive).
    # initialize door list with all goats
    door_list = [goat] * num_doors

    # Randomly choose the door hiding the prize (car).
    winning_door = random.randint(0, num_doors-1)
    door_list[winning_door] = car
    if verbose:
        print('DOOR {} \t\tPrize behind door {} '.format(door_list,winning_door+1),end='')

    # The contestant picks a random door, too.
    choice = random.randint(0, num_doors-1)
    if verbose:
        print('Contestant door {} ({}) '.format(choice+1,door_list[choice]),end='')


    # The host opens all but two doors, contestant choice and the car door if the price was not chosen
    if (choice != winning_door): 
        last_door = winning_door
    else:    
        # or a randomly selected one if the choice was the car
        last_door = random.randint(0, num_doors-1)
        while (last_door == choice):
            last_door = random.randint(0, num_doors-1)
    
    if verbose:
        print('\tHost opens all door except {} and {} '.format(choice+1,last_door+1),end='')
    
    # the Martian must choose between these 2 doors
    martian_door = random.choice((last_door,choice))
    if verbose: 
        print('Martian chose {}'.format(martian_door+1))

    # Does the contestant want to switch their choice?
    if switch:
        if verbose:
            print('Contestant switches from door {} to {} '.format(choice+1,last_door+1))
        choice = last_door

    # Did the contestant win?
    won  = (choice == winning_door)
    mwon = (martian_door == winning_door)
    if verbose:
        print('Contestant win={}. Martian win={}'.format(won,mwon))
    return [won,mwon]


def main():
    # Get command-line arguments
    parser = argparse.ArgumentParser(
        description='simulate the Monty Hall problem with Martian making choice')
    parser.add_argument('--doors', default=3, type=int, metavar='int',
                        help='number of doors offered to the contestant')
    parser.add_argument('--trials', default=10000, type=int, metavar='int',
                        help='number of trials to perform')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='display the results of each trial')
    args = parser.parse_args()

    print('Simulating {:,} trials...'.format(args.trials))

    # Carry out the trials
    winning_non_switchers   = 0
    winning_switchers       = 0
    winning_nonsw_martian   = 0
    winning_switch_martian  = 0
    
    for i in range(args.trials):
        # First, do a trial where the contestant never switches.
        lwon = simulate(args.doors, switch=False, verbose=args.verbose)
        if lwon[0]:
            winning_non_switchers += 1
        if lwon[1]:
            winning_nonsw_martian += 1

        # Next, try one where the contestant switches.
        lwon = simulate(args.doors, switch=True, verbose=args.verbose)
        if lwon[0]:
            winning_switchers += 1
        if lwon[1]:
            winning_switch_martian += 1

    print('    Switching won {0:5,} / {1:,} ({2:.5}% of the time)'.format(
            winning_switchers, args.trials,
            (winning_switchers / args.trials * 100 ) ))
    print('    Martian   won {0:5,} / {1:,} ({2:.5}% of the time)'.format(
            winning_switch_martian, args.trials,
            (winning_switch_martian / args.trials * 100 ) ))

    print('Not switching won {0:5,} / {1:,} ({2:.5}% of the time)'.format(
            winning_non_switchers, args.trials,
            (winning_non_switchers / args.trials * 100 ) ))
    print('    Martian   won {0:5,} / {1:,} ({2:.5}% of the time)'.format(
            winning_nonsw_martian, args.trials,
            (winning_nonsw_martian / args.trials * 100 ) ))


if __name__ == '__main__':
    main()