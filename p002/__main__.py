#!/usr/bin/env python
# -*- coding: utf-8 -*-
from project_euler.euler import euler


@euler(pid=2, update_readme=True)
def solve():
    # build up all fibonacci values
    fib = [1, 2, 3]
    while fib[-1] <= 4000000:
        fib += [fibonaccify(n1=fib[-1], n2=fib[-2])]

    # sum all even values
    evens = []
    for i in fib[:-1]:
        if i % 2 == 0:
            evens += [i]

    return sum(evens)


def fibonaccify(n1, n2):
    return n1 + n2


if __name__ == '__main__':
    solve()
