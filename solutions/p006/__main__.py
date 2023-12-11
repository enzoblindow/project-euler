#!/usr/bin/env python
# -*- coding: utf-8 -*-
from euler import euler


@euler(pid=6, update_readme=False)
def solve():
    sum_of_squares = sum(i**2 for i in range(1, 101))
    sum_squared = sum(range(1, 101))**2

    return sum_squared - sum_of_squares


if __name__ == '__main__':
    print(solve())

    