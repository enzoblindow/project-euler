#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from euler import euler


PRIMES = list()


def prime_list(num):
    primes = []
    for prime in range(2, num + 1):
        # Assume number is prime until shown it is not.
        is_prime = True
        for num_ in range(2, int(prime ** 0.5) + 1):
            if prime % num_ == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(prime)

    return (primes)


def is_prime(num):
    for num_ in range(2, int(num ** 0.5) + 1):
        if num % num_ == 0:
            return False
    return True


def divide_by_prime(num, by, prime_dividends):
    print('Finding next prime factor for', num, 'starting to divide at ', by)

    div = float(num) / by

    if not div % 1 == 0:
        divide_by_prime(num, prime_dividends[prime_dividends.index(by)+1], prime_dividends)
        return

    print('Prime dividend:', by, 'produces', div)

    if is_prime(div):
        PRIMES.append(int(by))
        PRIMES.append(int(div))
        print('End of recursion')
        return
    else:
        PRIMES.append(int(by))
        print('Current prime factors found:', PRIMES)
        divide_by_prime(div, prime_dividends[0], prime_dividends)


@euler(pid=3, update_readme=True)
def solve(num):
    divide_by_prime(num, 2, prime_list(100000))
    return PRIMES


if __name__ == '__main__':
    PRIMES = list()
    val = 600851475143
    print(solve(val))
    res = reduce(lambda x, y : x * y, PRIMES)
    if res == val:
        print('Largest prime factor is', max(PRIMES))
    else:
        print('Something went wrong')
