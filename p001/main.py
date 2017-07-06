#!/usr/bin/env python
# -*- coding: utf-8 -*-

MULTIPLES = [3, 5]

def is_multiple(num):
    for multiple in MULTIPLES:
        if num % multiple == 0:
            return True
    return False

def solve(num):
    return sum([i for i in range(num) if is_multiple(i)])

if __name__ == '__main__':
    answer = solve(1000)
    print 'Problem: Find the sum of all the multiples of 3 or 5 below 1000.'
    print 'Solution: {}'.format(answer)
