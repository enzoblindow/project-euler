#!/usr/bin/env python
# -*- coding: utf-8 -*-
from euler import euler


DIVIDENDS_TO_CHECK = range(10, 21)  # All values between 1-10 will be divisible when its divisible for these numbers

def has_no_remainder(n, m):
    if n % float(m) == 0:
        return True
    else:
        return False

def no_remainders(val):
    for n in DIVIDENDS_TO_CHECK[::-1]:
        if has_no_remainder(val, n):
            continue
        else:
            return False
    return True


@euler(pid=5, update_readme=True)
def solve():
    i = 20.0
    while True:
        if no_remainders(i):
            return int(i)
        i += 20  # we can safely increment by 20, as otherwise not all dividends have no remainders


if __name__ == '__main__':
    print solve()
