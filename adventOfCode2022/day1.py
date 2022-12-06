import sys
from typing import Iterable, List


def parse(input_stream: Iterable[str]) -> List[List[int]]:
    elves = [[]]
    for s in input_stream:
        if s.strip():
            elves[-1].append(int(s.strip()))
        else:
            elves.append([])
    return elves


def solve():
    if sys.argv[1] == 'part1':
        elves = parse(sys.stdin)
        calories = [sum(food) for food in elves]
        return max(calories)
    if sys.argv[1] == 'part2':
        elves = parse(sys.stdin)
        calories = sorted([sum(food) for food in elves])
        return sum(calories[-3:])


if __name__ == '__main__':
    print(solve())
