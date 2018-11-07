#!/usr/bin/env python
# -*- coding: utf-8 -*-
from euler import euler


def is_palindrome(number):
    number = str(number)
    a = number[:3]
    b = number[3:]

    return a == b[::-1]


@euler(pid=4, update_readme=True)
def solve():
    results = list()
    firsts = range(100, 1000)[::-1]
    seconds = range(100, 1000)[::-1]

    for first in firsts:
        for second in seconds:
            number = first * second
            if is_palindrome(number):
                results.append(number)

    return max(results)


if __name__ == '__main__':
    print solve()

    