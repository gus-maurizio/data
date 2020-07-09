#!/usr/bin/env python3

##### common alphabet
import numpy as np
import matplotlib.pyplot as plt

import random
import functools

def common(a,b):
    return (set(a) & set(b))

common('stringsupper','piers')


##### is an integer base 2 a palindrome?

def palindrome(a):
    base2_a = bin(a)[2:]
    return (base2_a == base2_a[::-1])

palindrome(8)
palindrome(9)


#### compute longest chain of links
list = [    ['Item1', 'Item2'],
            ['Item2', 'Item3'],
            ['Item2', 'Item4'],
            ['Item3', 'Item4'],
            ['Item3', 'Item5'],
            ['Item5', 'Item7'],
            ['Item6', 'Item8']]

dict    =   {}
for (x,y) in list:
    print(x,y)
    if x not in dict: dict[x] = []
    dict[x].append(y)

for x in dict:
    for y in dict[x]:
        if y in dict:
            print(x,y)
            dict[x].extend(dict[y])

### remove duplicates from using lists by sets
for x in dict:
    dict[x] = set(dict[x])

max = 0
who = 0
for x in dict:
    if len(dict[x]) > max:
        max = len(dict[x])
        who = x

print('Max items',who,dict[who])


#### queue
import queue
import threading

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        print(item)
        q.task_done()

q = queue.Queue()
num_worker_threads = 4
threads = []
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in range(10):
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)

for t in threads:
    t.join()


