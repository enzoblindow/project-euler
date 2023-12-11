#!/usr/bin/env python
# -*- coding: utf-8 -*-
from euler import euler


def is_palindrome(num):
    return str(num)[:3] == str(num)[3:][::-1]


@euler(pid=4, update_readme=True)
def solve():
    max = 0
    firsts = range(100, 1000)[::-1]
    seconds = range(100, 1000)[::-1]

    for first in firsts:
        for second in seconds:
            number = first * second

            if number < max:
                break

            if is_palindrome(number):
                if number > max:
                    max = number
                    break

    return max


if __name__ == '__main__':
    print(solve())
