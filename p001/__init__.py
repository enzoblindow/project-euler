#!/usr/bin/env python
# -*- coding: utf-8 -*-

from project_euler.euler import euler

MULTIPLES = [3, 5]

def is_multiple(num):
    for multiple in MULTIPLES:
        if num % multiple == 0:
            return True
    return False

@euler(pid=1, update_readme=True)
def solve(num):
    return sum([i for i in range(num) if is_multiple(i)])

if __name__ == '__main__':
    solve(1000)
