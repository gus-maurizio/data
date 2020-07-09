#!/usr/bin/env python3
import random
import math

## library of functions and examples for Probability and Statistics
## Follows examples and exercises from Henk Tijms - Understanding Probability

# given a probability, returns true or false with same distribution. Use p = 0.5 for coin tosses (true or false)
def generate(p):
    return random.random() >= p


# simple Monte Carlo (MC) style for 1,000,000 tries
sum(generate(0.5) for i in range(1000000))
