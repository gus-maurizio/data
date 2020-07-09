#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


d1 = np.random.random_integers(1, 6, 1000)
d2 = np.random.random_integers(1, 6, 1000)
dsums = d1 + d2

count, bins, ignored = plt.hist(dsums, 11, normed=True)
plt.show()
