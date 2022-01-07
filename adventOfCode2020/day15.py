import sys
from typing import Dict


def get_nth_spoken_number(nth: int, numbers: Dict[int, int]) -> int:
    last_round, last_number = max((i, n) for (n, i) in numbers.items())
    previous_numbers = {}

    for i in range(last_round + 1, nth):
        if last_number in previous_numbers:
            last_number = numbers[last_number] - previous_numbers[last_number]
        else:
            last_number = 0
        if last_number in numbers:
            previous_numbers[last_number] = numbers[last_number]
        numbers[last_number] = i
    return last_number


def solve():
    numbers = {}
    for (i, n) in enumerate(sys.stdin.readline().strip().split(",")):
        numbers[int(n)] = i

    if sys.argv[1] == 'part1':
        return get_nth_spoken_number(2020, numbers)
    if sys.argv[1] == 'part2':
        return get_nth_spoken_number(30000000, numbers)


if __name__ == '__main__':
    print(solve())
