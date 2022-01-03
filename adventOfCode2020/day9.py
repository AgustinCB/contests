import sys
from typing import List


def first_invalid_number(numbers: List[int], preamble: int) -> int:
    for i in range(preamble, len(numbers)):
        number = numbers[i]
        candidates = set(numbers[i - preamble:i])
        if not any(abs(number - candidate) in candidates - {candidate} for candidate in candidates):
            return number


def first_continuous_set_adding_to(numbers: List[int], target: int) -> int:
    starting_range = 0
    ending_range = 1
    sum_so_far = numbers[starting_range] + numbers[ending_range]

    while sum_so_far != target:
        ending_range += 1
        sum_so_far += numbers[ending_range]
        while sum_so_far > target:
            sum_so_far -= numbers[starting_range]
            starting_range += 1

    minimum = min(numbers[starting_range:ending_range + 1])
    maximum = max(numbers[starting_range:ending_range + 1])
    return minimum + maximum


def solve():
    numbers = []
    for line in sys.stdin:
        numbers.append(int(line.strip()))

    if sys.argv[1] == 'part1':
        return first_invalid_number(numbers, int(sys.argv[2]))
    if sys.argv[1] == 'part2':
        target = first_invalid_number(numbers, int(sys.argv[2]))
        return first_continuous_set_adding_to(numbers, target)


if __name__ == '__main__':
    print(solve())
