import sys
from typing import Tuple


def find_marker(s: str, distance: int) -> Tuple[int, str]:
    for i in range(len(s) - 3):
        chars = set(list(s[i:i+distance]))
        if len(chars) == distance:
            return i + distance, s[i:i+distance]


def solve():
    if sys.argv[1] == 'part1':
        return find_marker(sys.stdin.readline(), 4)[0]
    if sys.argv[1] == 'part2':
        return find_marker(sys.stdin.readline(), 14)[0]


if __name__ == '__main__':
    print(solve())
