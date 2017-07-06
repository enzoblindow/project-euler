"""
Class based approach which uses a number class for each position in the Problem
for tracking.
"""
from itertools import combinations

LEGAL_VALUES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

class Digit(object):
    """Single digit in an array of digit, which build up the problem"""
    def __init__(self, index):
        self.solved = None
        self.index = index
        self.values = LEGAL_VALUES

    def remove(self, val):
        self.values = [value for value in self.values if value != val]

    def solve(self, val):
        self.solved = val
        self.values = [val]

class Sequence(object):
    """Problem is an array of n Digits"""
    def __init__(self, length):
        self.digits = [Digit(index=i) for i in range(length)]

    def remove_all(self, num):
        for idx, val in enumerate(map(int, str(num))):
            self.digits[idx].remove(val)


def solve(length, guesses):
    seq = Sequence(length)

    # Easy first, remove all values for digits from guesses with 0 correct
    for guess in guesses:
        if guess[1] == 0:
            seq.remove_all(guess[0])
            guesses.remove(guess)

    # Then find guesses where the sum of correct guesses exceed the length by 1
    combinations = sum([map(list, combinations(guesses, i)) for i in range(len(guesses) + 1)], [])
    for combination in combinations:
        _sum = sum([pair[1] for pair in combination])
        if _sum == length + 1:
            print combination
            r = {key: [] for key in range(length)}
            com_len = len(combination)
            for guess in combination:
                for idx, val in enumerate(map(int, str(guess[0]))):
                    r[idx] += [val]
            for i in range(length):
                counts = [[x,r[i].count(x)] for x in set(r[i])]
                print counts

            print r



solve(5, guesses)


if __name__ == '__main__':
    # 5-digit example problem
    guesses = [
        (90342, 2),
        (70794, 0),
        (39458, 2),
        (34109, 1),
        (51545, 2),
        (12531, 1),
    ]
